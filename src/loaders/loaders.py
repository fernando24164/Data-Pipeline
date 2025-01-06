import datetime
from typing import Generator, TypedDict

from clients.athena_client import AthenaClient
from clients.s3_client import S3Client


class SalesLoader:
    def __init__(self, role_arn: str, bucket_name="sales-data") -> None:
        self.s3_client = S3Client(role_arn)
        self.bucket_name = bucket_name

    def get_sales(self, time_period: int) -> Generator:
        """
        Get sales data from S3 for a given time period.
        """
        today = datetime.date.today()
        for index, day in enumerate(range(time_period)):
            date = today - datetime.timedelta(days=day)
            file_name = f'sales_{date.strftime("%m-%d")}.csv'
            try:
                response = self.s3_client.get_object(self.bucket_name, file_name)
                # before yield remove the headers except for the first file
                if index == 0:
                    yield response["Body"].read().decode("utf-8").split("\n")
                else:
                    yield response["Body"].read().decode("utf-8").split("\n")[1:]

            except Exception as e:
                print(f"Error loading sales data for {date}: {e}")
                continue


class QueryParams(TypedDict):
    """
    Type definition for query parameters used in customer session queries.
    """

    start_time: str
    end_time: str
    customer_id: str


class CustomerSession:
    def __init__(self, role_arn: str):
        self.athena_client = AthenaClient(role_arn)
        with open("customer_session.sql", "r") as f:
            self.query = f.read()

    def get_customer_sessions(self, query_params: QueryParams) -> Generator:
        """
        Execute a query on Athena to get customer sessions.
        """
        self.query = self.query.format(**query_params)
        try:
            response_id = self.athena_client.execute_query(self.query)
            yield self.athena_client.get_query_results(response_id)
        except Exception as e:
            print(f"Error executing query: {e}")
