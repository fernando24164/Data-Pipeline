import pandas as pd
from sqlalchemy.types import Float, Integer

from src.clients.postgres_client import PostgresClient


class PostgresExporter:
    def __init__(self, arn_role: str) -> None:
        self.client = PostgresClient(arn_role)

    def export_customer_sells(self, df: pd.DataFrame, chunk_size: int = 10000) -> None:
        """Export a pandas DataFrame to a PostgreSQL table.
        Only total_session_time, avg_product_sales, and customer_id will be exported.
        """
        table_name = "customer_sells"
        columns = ["total_session_time", "avg_product_sales", "customer_id"]
        dtype = {
            "total_session_time": Float,
            "avg_product_sales": Float,
            "customer_id": Integer,
        }

        try:
            df[columns].to_sql(
                table_name,
                self.client.get_session().connection(),
                if_exists="replace",
                index=False,
                chunksize=chunk_size,
                dtype=dtype,
                method="multi",
            )
        except Exception as e:
            print(f"Error exporting customer sells: {e}")
