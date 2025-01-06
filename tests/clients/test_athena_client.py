from unittest.mock import patch, MagicMock
from src.clients.athena_client import AthenaClient


@patch("boto3.Session")
def test_execute_query(mock_boto_session):
    mock_client = MagicMock()
    mock_boto_session.return_value.client.return_value = mock_client

    athena_client = AthenaClient(
        database="test_db",
        output_location="s3://test-bucket/",
        role_arn="arn:aws:iam::123456789012:role/test-role",
    )

    mock_client.start_query_execution.return_value = {
        "QueryExecutionId": "mock_execution_id"
    }

    query_execution_id = athena_client.execute_query("SELECT * FROM test_table")

    assert query_execution_id == "mock_execution_id"
    mock_client.start_query_execution.assert_called_once()


@patch("time.sleep", return_value=None)  # Mock time.sleep to avoid delays
@patch("boto3.Session")
def test_get_query_results(mock_boto_session, mock_sleep):
    mock_client = MagicMock()
    mock_boto_session.return_value.client.return_value = mock_client

    athena_client = AthenaClient(
        database="test_db",
        output_location="s3://test-bucket/",
        role_arn="arn:aws:iam::123456789012:role/test-role",
    )

    mock_client.get_query_execution.return_value = {
        "QueryExecution": {"Status": {"State": "SUCCEEDED"}}
    }

    mock_paginator = mock_client.get_paginator.return_value
    mock_paginator.paginate.return_value = [
        {
            "ResultSet": {
                "Rows": [
                    {
                        "Data": [
                            {"VarCharValue": "row1_col1"},
                            {"VarCharValue": "row1_col2"},
                        ]
                    },
                    {
                        "Data": [
                            {"VarCharValue": "row2_col1"},
                            {"VarCharValue": "row2_col2"},
                        ]
                    },
                ]
            }
        }
    ]

    results = list(athena_client.get_query_results("mock_execution_id"))

    expected_results = [["row1_col1", "row1_col2"], ["row2_col1", "row2_col2"]]
    assert results == expected_results
    mock_client.get_query_execution.assert_called_once_with(
        QueryExecutionId="mock_execution_id"
    )
    mock_client.get_paginator.assert_called_once_with("get_query_results")
