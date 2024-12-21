from typing import BinaryIO
import pandas as pd
from io import BytesIO
import boto3

from src.clients.mixins.token_manager import TokenManagerMixin


class S3Client(TokenManagerMixin):
    def __init__(self, role_arn: str) -> None:
        """
        Initialize the S3 client using the specified role ARN.

        Args:
            role_arn: AWS IAM role ARN for authentication
        """
        super().__init__(role_arn)
        self.refresh_credentials()
        self.s3 = self.session.client("s3")

    def upload_file_in_memory(
        self, file_obj: BinaryIO, bucket_name: str, object_name: str
    ) -> None:
        """
        Upload a file-like object to an S3 bucket.

        Args:
            file_obj: File-like object to upload (e.g., BytesIO)
            bucket_name: Name of the S3 bucket
            object_name: S3 object name
        """
        self.refresh_credentials()
        try:
            self.s3.put_object(Bucket=bucket_name, Key=object_name, Body=file_obj)
        except Exception as e:
            raise RuntimeError(f"Failed to upload file to S3: {str(e)}") from e

    def download_file_as_dataframe(
        self, bucket_name: str, object_name: str
    ) -> pd.DataFrame:
        """
        Download a file from S3 and return it as a Pandas DataFrame.

        Args:
            bucket_name: Name of the S3 bucket
            object_name: S3 object name

        Returns:
            DataFrame containing the data from the downloaded file

        Raises:
            RuntimeError: If download or DataFrame conversion fails
        """
        self.refresh_credentials()
        try:
            response = self.s3.get_object(Bucket=bucket_name, Key=object_name)
            file_content = response["Body"].read()
            return pd.read_csv(BytesIO(file_content))
        except Exception as e:
            raise RuntimeError(f"Failed to download file from S3: {str(e)}") from e
