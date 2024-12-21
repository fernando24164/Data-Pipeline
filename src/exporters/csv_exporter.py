import pandas as pd


def export_to_csv(df, file_path):
    """
    Export the DataFrame to a CSV file.

    Parameters:
    - df: DataFrame, the DataFrame to export
    - file_path: str, path to save the CSV file
    """
    df.to_csv(file_path, index=False)
