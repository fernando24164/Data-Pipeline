import pandas as pd

from clients.postgres_client import PostgresClient


class PostgresExporter:
    def __init__(self, arn_role: str) -> None:
        self.client = PostgresClient(arn_role)

    def export_customer_sells(self, df: pd.DataFrame) -> None:
        """Export a pandas DataFrame to a PostgreSQL table."""
        table_name = "customer_sells"
        
        df.to_sql(
            table_name,
            self.client.get_session().connection(),
            if_exists="replace",
            index=False
        )