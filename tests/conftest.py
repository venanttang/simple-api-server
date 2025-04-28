import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlalchemy import text


# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

# Create an in-memory SQLite database for testing
# test_engine = create_engine("sqlite:///file:shared?mode=memory&cache=shared&uri=true", 
#                             echo=False, 
#                             pool_pre_ping=True,
#                             connect_args={
#                                 "check_same_thread": False,
#                                 "timeout": 30,
#                                 }
#                             )
# sqlite_file = "test.db"
# test_engine = create_engine(f"sqlite:///{sqlite_file}", echo=False)

# Set the SQLite database file name
sqlite_file = "database_test.db"
# TODO: change to memory mode later...
# ...

# Create the SQLite database engine
test_engine = create_engine(f"sqlite:///{sqlite_file}", 
                       echo=False, 
                       pool_pre_ping=True,
                       connect_args={
                           "check_same_thread": False,
                           "timeout": 30,
                           }
                       )

# Execute a PRAGMA to enable WAL mode for SQLite to improve concurrency
def enable_wal():
    with test_engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL;"))

enable_wal()


@pytest.fixture(name="client")
def client_fixture(monkeypatch):
    # Override the engine in the main app with the test engine
    monkeypatch.setattr("main.engine", test_engine)
    SQLModel.metadata.create_all(test_engine)
    with TestClient(app) as client:
        yield client
    # Clean up the database after tests
    # SQLModel.metadata.drop_all(test_engine)

# from typing import Generator

# def yieldTestClient() -> Generator[TestClient, None, None]:
#     # Create a TestClient instance for testing
#     with TestClient(app) as client:
#         yield client
