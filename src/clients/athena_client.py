from typing import Iterator, List, Optional
import time

from src.clients.mixins.token_manager import TokenManagerMixin


class AthenaClient(TokenManagerMixin):
    """Client for executing queries and retrieving results from Amazon Athena."""

    TERMINAL_STATES = {"SUCCEEDED", "FAILED", "CANCELLED"}
    POLL_INTERVAL = 1  # seconds

    def __init__(
        self, database: str, output_location: str, role_arn: str = None
    ) -> None:
        """
        Initialize Athena client with database and output location.

        Args:
            database: Target Athena database name
            output_location: S3 location for query results
            profile_name: AWS credentials profile name
        """
        super().__init__(role_arn)
        self.database = database
        self.output_location = output_location

        self.refresh_credentials()
        self.client = self.session.client("athena")

    def execute_query(self, query: str) -> str:
        """
        Execute a query and return the query execution ID.

        Args:
            query: SQL query to execute

        Returns:
            Query execution ID
        """
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": self.database},
            ResultConfiguration={"OutputLocation": self.output_location},
        )
        return response["QueryExecutionId"]

    def get_query_results(
        self, query_execution_id: str
    ) -> Iterator[List[Optional[str]]]:
        """
        Fetch query results and yield rows as a generator.

        Args:
            query_execution_id: ID of the query execution to fetch results for

        Yields:
            List of values for each row

        Raises:
            Exception: If query execution fails
        """
        while True:
            status = self.client.get_query_execution(
                QueryExecutionId=query_execution_id
            )["QueryExecution"]["Status"]["State"]

            if status in self.TERMINAL_STATES:
                break

            time.sleep(self.POLL_INTERVAL)

        if status != "SUCCEEDED":
            raise Exception(f"Query failed with status: {status}")

        paginator = self.client.get_paginator("get_query_results")
        for page in paginator.paginate(QueryExecutionId=query_execution_id):
            for row in page["ResultSet"]["Rows"]:
                yield [data.get("VarCharValue") for data in row["Data"]]
