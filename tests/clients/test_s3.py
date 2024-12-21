
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from src.clients.s3_client import S3Client

from datetime import datetime, timezone, timedelta
from io import BytesIO



def test_init_with_valid_role_arn(mocker):
    role_arn = "arn:aws:iam::123456789012:role/test-role"
    mock_session = mocker.Mock()
    mock_session.client.return_value = mocker.Mock()

    mock_sts = mocker.Mock()
    mock_sts.assume_role.return_value = {
        "Credentials": {
            "AccessKeyId": "test-key",
            "SecretAccessKey": "test-secret",
            "SessionToken": "test-token",
            "Expiration": datetime.now(timezone.utc) + timedelta(hours=1)
        }
    }
    mocker.patch("boto3.client", return_value=mock_sts)
    mocker.patch("boto3.Session", return_value=mock_session)

    s3_client = S3Client(role_arn)

    # Assert
    assert s3_client.role_arn == role_arn
    assert s3_client.session == mock_session
    assert s3_client.s3 == mock_session.client.return_value
    mock_sts.assume_role.assert_called_once_with(
        RoleArn=role_arn,
        RoleSessionName="S3ClientSession"
    )

def test_upload_file_in_memory_success(mocker):
    role_arn = "arn:aws:iam::123456789012:role/test-role"
    bucket = "test-bucket"
    key = "test/file.txt"
    data = b"test data"
    file_obj = BytesIO(data)
    expiration_time = datetime.now(timezone.utc) + timedelta(hours=1)

    mock_credentials = {
        "Credentials": {
            "AccessKeyId": "test-access-key",
            "SecretAccessKey": "test-secret-key",
            "SessionToken": "test-session-token",
            "Expiration": expiration_time
        }
    }

    mock_sts = mocker.Mock()
    mock_sts.assume_role.return_value = mock_credentials

    mock_s3 = mocker.Mock()
    mock_session = mocker.Mock()
    mock_session.client.return_value = mock_s3

    mocker.patch("boto3.client", return_value=mock_sts)
    mocker.patch("boto3.Session", return_value=mock_session)

    s3_client = S3Client(role_arn)
    s3_client.upload_file_in_memory(file_obj, bucket, key)

    mock_s3.put_object.assert_called_once_with(
        Bucket=bucket,
        Key=key,
        Body=file_obj
    )