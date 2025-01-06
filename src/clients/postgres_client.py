from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from clients.mixins.secret_manager import AwsSecretMixin
from clients.mixins.token_manager import TokenManagerMixin


class PostgresClient(AwsSecretMixin):
    """PostgreSQL database client with connection pooling and session management."""

    def __init__(self, role_arn: str) -> None:
        super().__init__(role_arn)
        self.engine: Engine = create_engine(
            self.database_url, pool_size=10, max_overflow=20, pool_pre_ping=True
        )
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def get_session(self) -> Session:
        """Get a new database session.

        Returns:
            Session: New SQLAlchemy session object
        """
        return self.Session()

    def close_session(self) -> None:
        """Close and remove the current session."""
        self.Session.remove()

    def execute_query(self, query: str, params: Optional[dict] = None) -> List[tuple]:
        """Execute a SQL query and return the results.

        Args:
            query: SQL query string to execute
            params: Optional dictionary of query parameters

        Returns:
            List of result tuples

        Raises:
            Exception: If query execution fails
        """
        session = self.get_session()
        try:
            result = session.execute(query, params or {})
            session.commit()
            return result.fetchall()
        except Exception:
            session.rollback()
            raise
        finally:
            self.close_session()
