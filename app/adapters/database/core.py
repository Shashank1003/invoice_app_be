from contextvars import ContextVar

from sqlalchemy import create_engine
from sqlalchemy.exc import InternalError, OperationalError
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

db_username = os.getenv("DATABASE_USERNAME")
db_password = os.getenv("DATABASE_PASSWORD")
db_hostname = os.getenv("DATABASE_HOSTNAME")
db_port = os.getenv("DATABASE_PORT")
db_name = os.getenv("DATABASE_NAME")
db_query = os.getenv("DATABASE_QUERY_PARAM")

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}?{db_query}"

DATABASE_ENGINE = create_engine(SQLALCHEMY_DATABASE_URL)


class SQLAlchemyConnector:
    """Central place to manage database connections, with context manager in place for below reasons:
    1. Explicit Control:  explicitly set and get the session within a specific context
    2. compatibility with async framework: single thread may handle multiple concurrent requests.

    Wanted to avoid the with operator and replace code everywhere, hence a shortcut.
    It may seem redundant as it is getting intialized everytime . But still a central place to manage.
    """

    def __init__(self, engine=DATABASE_ENGINE):
        self.engine = engine
        self.session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )
        self.SessionLocal = scoped_session(session_factory=self.session_factory)
        self.db_session_var = ContextVar("db_session")
        self.base = declarative_base()

    def get_db_session(self):
        try:
            db_session = self.SessionLocal()
            self.db_session_var.set(db_session)
        except (InternalError, OperationalError):
            self.SessionLocal.remove()
            db_session = self.SessionLocal()
            self.db_session_var.set(db_session)
        return db_session

    def get_current_db_session(self):
        return self.db_session_var.get()

    # noinspection PyUnresolvedReferences
    def create_all(self, engine=None):
        if engine is None:
            engine = self.engine
        self.base.metadata.create_all(bind=engine)

    def get_base(self):
        return self.base
