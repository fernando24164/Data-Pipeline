import pandas as pd


def load_csv(file_path):
    """
    Load a CSV file into a Pandas DataFrame.

    Parameters:
    - file_path: str, path to the CSV file

    Returns:
    - DataFrame: Loaded data as a Pandas DataFrame
    """
    return pd.read_csv(file_path)
