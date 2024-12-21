from datetime import datetime, timezone
from typing import Optional
import boto3
from boto3.session import Session
from mypy_boto3_sts.client import STSClient


class TokenManagerMixin:
    def __init__(self, role_arn: str) -> None:
        self.role_arn: str = role_arn
        self.expiricy: Optional[datetime] = None
        self.session: Optional[Session] = None

    def _is_token_expired(self) -> bool:
        """
        Check if the current token is expired.
        """
        if self.expiricy is None:
            return True
        return self.expiricy < datetime.now(timezone.utc)

    def refresh_credentials(self) -> None:
        """
        Refresh the credentials if they are expired.
        """
        if self._is_token_expired():
            sts_client: STSClient = boto3.client("sts")
            assumed_role = sts_client.assume_role(
                RoleArn=self.role_arn, RoleSessionName="S3ClientSession"
            )
            credentials = assumed_role["Credentials"]

            self.expiricy = credentials["Expiration"]
            self.session = boto3.Session(
                aws_access_key_id=credentials["AccessKeyId"],
                aws_secret_access_key=credentials["SecretAccessKey"],
                aws_session_token=credentials["SessionToken"],
            )
