import boto3
from botocore.exceptions import ClientError


class AwsSecretMixin:
    """
    Mixin to manage AWS Secrets Manager connection and obtain the Aurora DB URL.
    """

    def __init__(
        self,
        role_arn: str,
        secret_arn: str = "arn:aws:secretsmanager:eu-central-1:123456789012:secret:MySecretName-a1b2c3",
        region_name: str = "eu-central-1",
    ):
        self.secret_arn = secret_arn
        self.region_name = region_name
        self.role_arn = role_arn
        self._session = self._get_aws_session()
        self._secrets_client = self._session.client(
            "secretsmanager", region_name=self.region_name
        )
        self._database_url = self._get_database_url()

    def _get_aws_session(self):
        """
        Create an AWS session using the provided role ARN or default credentials.
        """
        if self.role_arn:
            sts_client = boto3.client("sts")
            try:
                assumed_role = sts_client.assume_role(
                    RoleArn=self.role_arn, RoleSessionName="AssumeRoleSession"
                )
                credentials = assumed_role["Credentials"]
                return boto3.Session(
                    aws_access_key_id=credentials["AccessKeyId"],
                    aws_secret_access_key=credentials["SecretAccessKey"],
                    aws_session_token=credentials["SessionToken"],
                )
            except ClientError as e:
                raise Exception(f"Error assuming role: {e}")
        else:
            return boto3.Session()

    def _get_database_url(self) -> str:
        """
        Retrieve the database URL from AWS Secrets Manager.
        """
        try:
            secret_value = self._secrets_client.get_secret_value(
                SecretId=self.secret_arn
            )
            secret_string = secret_value["SecretString"]

            return secret_string
        except ClientError as e:
            raise Exception(f"Error retrieving secret: {e}")

    @property
    def database_url(self) -> str:
        """
        Return the database URL.
        """
        return self._database_url
