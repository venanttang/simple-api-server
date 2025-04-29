import logging
import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlalchemy import text

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

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
    try:
        with test_engine.connect() as conn:
            logger.info("Enabling WAL mode for SQLite")
            conn.execute(text("PRAGMA journal_mode=WAL;"))
    except Exception as e:
        logger.error(f"Failed to enable WAL mode: {e.__class__.__name__}: {e}")

enable_wal()

# @pytest.fixture(name="client")
# def client_fixture(monkeypatch):
#     # Override the engine in the main app with the test engine
#     monkeypatch.setattr("main.engine", test_engine)
#     SQLModel.metadata.create_all(test_engine)
#     with TestClient(app) as client:
#         yield client
#     # Clean up the database after tests
#     # SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client")
def client_fixture(replace_db, db_setup):
    # Override the engine in the main app with the test engine
    # monkeypatch.setattr("main.engine", test_engine)
    # SQLModel.metadata.create_all(test_engine)
    with TestClient(app) as client:
        logger.info("----------Creating the test client----------")
        yield client
        logger.info("----------Tearing down the test client----------")
    # Clean up the database after tests
    # SQLModel.metadata.drop_all(test_engine)
    
@pytest.fixture(scope="module", name="db_setup")
def db_setup_fixture():
    logger.info("----------Setting up the test database----------")
    # Override the engine in the main app with the test engine
    # monkeypatch.setattr("main.engine", test_engine)
    SQLModel.metadata.create_all(test_engine)
    yield "create DB"
    logger.info("----------Tearing down the test database----------")
    # Clean up the database after tests
    SQLModel.metadata.drop_all(test_engine)
    
@pytest.fixture(name="replace_db")
def replace_db_fixture(monkeypatch):
    logger.info("----------Replacing the engine----------")
    # Override the engine in the main app with the test engine
    monkeypatch.setattr("main.engine", test_engine)
    yield "engine replaced"
    logger.info("----------Done with the engine----------")



# from typing import Generator

# def yieldTestClient() -> Generator[TestClient, None, None]:
#     # Create a TestClient instance for testing
#     with TestClient(app) as client:
#         yield client
