import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

# Create an in-memory SQLite database for testing
test_engine = create_engine("sqlite:///file:shared?mode=memory&cache=shared&uri=true", 
                            echo=False, 
                            pool_pre_ping=True,
                            connect_args={
                                "check_same_thread": False,
                                "timeout": 30,
                                }
                            )
# sqlite_file = "test.db"
# test_engine = create_engine(f"sqlite:///{sqlite_file}", echo=False)

@pytest.fixture(name="client")
def client_fixture(monkeypatch):
    # Override the engine in the main app with the test engine
    monkeypatch.setattr("main.engine", test_engine)
    SQLModel.metadata.create_all(test_engine)
    with TestClient(app) as client:
        yield client
    # Clean up the database after tests
    SQLModel.metadata.drop_all(test_engine)

