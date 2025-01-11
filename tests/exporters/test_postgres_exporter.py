from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.clients.postgres_client import PostgresClient
from src.exporters.postgres_exporter import PostgresExporter


@pytest.fixture
def test_df():
    return pd.DataFrame(
        {
            "total_session_time": [10, 20, 30],
            "avg_product_sales": [5, 10, 15],
            "customer_id": [1, 2, 3],
            "other_column": ["a", "b", "c"],
        }
    )


@patch("src.exporters.postgres_exporter.PostgresClient")
def test_export_customer_sells_pytest(MockPostgresClient, test_df):
    mock_client = MagicMock()
    mock_session = MagicMock()
    mock_connection = MagicMock()
    mock_session.connection.return_value = mock_connection
    mock_client.get_session.return_value = mock_session
    MockPostgresClient.return_value = mock_client

    exporter = PostgresExporter(arn_role="test_role")
    exporter.export_customer_sells(test_df)

    MockPostgresClient.assert_called_once_with("test_role")
    mock_client.get_session.assert_called_once()
