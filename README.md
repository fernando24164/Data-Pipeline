# 🚧 Data Pipeline Project: The Wild West of Data Wrangling 🤠 (WIP)

A simple data pipeline for loading, transforming, and exporting CSV data.

## Brief Description

This project is a data pipeline designed to load, transform, and export data from various sources (e.g., S3, Athena) to a PostgreSQL database. It is particularly focused on handling sales and customer session data, performing transformations, and exporting the results for further analysis. The pipeline is built with Python and leverages AWS services like S3, Athena, and Secrets Manager for data storage, querying, and secure credential management.

## Features

- **Data Loading**: Load data from S3 buckets and query data from Amazon Athena.
- **Data Transformation**: Perform transformations on sales and customer session data, including date parsing, aggregation, and merging.
- **Data Export**: Export transformed data to a PostgreSQL database.
- **AWS Integration**: Seamlessly integrate with AWS services using IAM roles and temporary credentials.
- **Modular Design**: The pipeline is designed with modular components (loaders, transformers, exporters) for easy extension and maintenance.
- **CLI Support**: Run the pipeline via a simple command-line interface.

## Installation Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/data-pipeline-project.git
   cd data-pipeline-project

2. Install Dependencies:
    Ensure you have Python 3.8+ installed. Then, install the required dependencies:

    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt  # For development and testing
    ```

3. Set Up AWS Credentials:
    Ensure your AWS credentials are configured, either via environment variables or the AWS CLI. The pipeline uses IAM roles for authentication, so ensure the role ARN is correctly specified in the config.json file.
    Configure the Pipeline:
    Modify the config.json file to include your AWS role ARN and region:

    ```json
    {
      "arn_role": "arn:aws:iam::123456789012:role/YourRole",
      "region": "eu-central-1"
    }
    ```

## Usage Examples
Running the Pipeline
To run the pipeline, use the provided CLI:

```bash
python -m src.cli
```

### Example Data Transformation
The pipeline performs the following transformations:

    Sales Data: Converts date strings to datetime objects, calculates total sales, and aggregates product sales.
    Customer Session Data: Parses session start times, calculates session durations, and merges with sales data.

### Exporting Data to PostgreSQL
The transformed data is exported to a PostgreSQL table named customer_sells. The table includes columns for total_session_time, avg_product_sales, and customer_id.
Configuration Options
The pipeline can be configured via the config.json file:

    arn_role: The AWS IAM role ARN used for authentication.
    region: The AWS region where your resources are located.

## Contribution Guidelines
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

Ensure your code passes all tests and follows the project's coding standards.

## Testing Instructions
To run the tests, use the following command:

```bash
pytest tests/
```
The test suite includes unit tests for the Athena client, S3 client, and PostgreSQL exporter. Mocking is used extensively to avoid dependencies on external services.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements/Credits

    AWS Boto3: For providing the Python SDK for AWS services.
    Pandas: For powerful data manipulation capabilities.
    SQLAlchemy: For database interaction and ORM support.
    Click: For building the command-line interface.

This project is under active development. Contributions and feedback are highly appreciated!