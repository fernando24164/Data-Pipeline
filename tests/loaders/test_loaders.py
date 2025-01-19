from unittest.mock import MagicMock, patch

from src.loaders.loaders import CustomerSession, QueryParams


# Method successfully executes query with valid QueryParams and yields results using a mocked AthenaClient with both role_arn and output_location.
@patch("src.loaders.loaders.AthenaClient")
def test_get_customer_sessions_success_with_mocked_athena_client_with_output_location(
    MockAthenaClient,
):
    # Arrange
    mock_athena = MagicMock()
    mock_athena.execute_query.return_value = "query-123"
    mock_athena.get_query_results.return_value = [["session1"], ["session2"]]
    MockAthenaClient.return_value = mock_athena

    query_params = QueryParams(
        start_time="2023-01-01", end_time="2023-01-02", customer_id="cust123"
    )

    customer_session = CustomerSession("role-arn")

    # Act
    result = list(customer_session.get_customer_sessions(query_params))

    # Assert
    mock_athena.execute_query.assert_called_once()
    mock_athena.get_query_results.assert_called_once_with("query-123")
    assert result == [[["session1"], ["session2"]]]
