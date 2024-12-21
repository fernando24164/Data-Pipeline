from src.loaders.csv_loader import load_csv
from src.transformations.data_transformer import transform_data
from src.exporters.csv_exporter import export_to_csv
from config.config import Config


def main():
    # Load configuration
    config = Config("config.json")  # Replace with your config JSON file path
    site_info = config.get_site_info()

    # Load data
    df = load_csv("input_data.csv")  # Replace with your input CSV file path

    # Transform data
    transformed_df = transform_data(df)

    # Export data
    export_to_csv(
        transformed_df, "output_data.csv"
    )  # Replace with your output CSV file path


if __name__ == "__main__":
    main()
