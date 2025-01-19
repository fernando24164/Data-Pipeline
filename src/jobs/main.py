import pandas as pd

from config.config import Config
from exporters.postgres_exporter import PostgresExporter
from loaders.loaders import CustomerSession, QueryParams, SalesLoader


def transform_sales_df(sales_df):
    sales_df["date"] = pd.to_datetime(sales_df["date"])
    sales_df["quantity"] = sales_df["quantity"].astype(int)
    sales_df["price"] = sales_df["price"].astype(float)

    sales_df["total_sales"] = sales_df["quantity"] * sales_df["price"]

    return sales_df


def transform_customer_session_df(customer_session_df):
    customer_session_df["session_start"] = pd.to_datetime(
        customer_session_df["session_start"]
    )
    customer_session_df["session_duration"] = customer_session_df[
        "session_duration"
    ].astype(float)

    customer_session_df["session_day"] = customer_session_df[
        "session_start"
    ].dt.day_name()
    customer_session_df["session_hour"] = customer_session_df["session_start"].dt.hour

    return customer_session_df


def merge_dataframes(sales_df, customer_session_df):
    merged_df = pd.merge(
        sales_df,
        customer_session_df,
        left_on=["date", "product_id"],
        right_on=[customer_session_df["session_start"].dt.date, "product_viewed"],
        how="inner",
    )

    merged_df["total_session_time"] = merged_df.groupby("customer_id")[
        "session_duration"
    ].transform("sum")
    merged_df["avg_product_sales"] = merged_df.groupby("product_id")[
        "total_sales"
    ].transform("mean")

    return merged_df


def main():
    # Load configuration
    config = Config()

    # Load data
    sales_data = list(
        SalesLoader(config.config_data.get("arn_role")).get_sales(time_period=7)
    )
    sales_df = pd.DataFrame(
        [row.split(",") for sublist in sales_data for row in sublist]
    )

    query_params = QueryParams(
        customer_id=1, start_time="21/02/2023", end_time="28/02/2023"
    )
    customer_session_data = CustomerSession(
        config.config_data.get("arn_role")
    ).get_customer_sessions(query_params)
    customer_session_df = pd.DataFrame(customer_session_data)

    # Transform data
    transformed_sales_df = transform_sales_df(sales_df)
    transformed_customer_session_df = transform_customer_session_df(customer_session_df)

    customer_sales_analysis = merge_dataframes(
        transformed_sales_df, transformed_customer_session_df
    )

    # Export data
    PostgresExporter(
        config.config_data.get("arn_role")
    ).export_customer_sells_to_postgres(customer_sales_analysis)
