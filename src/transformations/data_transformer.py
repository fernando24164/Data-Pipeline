import pandas as pd


def transform_data(df):
    """
    Transform the DataFrame by performing basic operations.

    Parameters:
    - df: DataFrame, the input DataFrame to transform

    Returns:
    - DataFrame: Transformed DataFrame
    """
    # Example transformation: drop rows with any missing values
    df = df.dropna()
    # Example transformation: rename columns (if needed)
    df.columns = [col.lower() for col in df.columns]
    return df
