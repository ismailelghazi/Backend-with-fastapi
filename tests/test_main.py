    import os
# Set env vars before importing app modules to ensure they use the test DB
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["POSTGRES_USER"] = "user"
os.environ["POSTGRES_PASSWORD"] = "password"
os.environ["POSTGRES_DB"] = "dbname"
os.environ["JWT_SECRET"] = "testsecret"
os.environ["HF_TOKEN"] = "testtoken"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.utils import hf_client
from unittest.mock import MagicMock

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Patch the app's engine to use our test engine
from app import database
database.engine = engine

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register():
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login():
    client.post(
        "/register",
        json={"username": "testuser2", "password": "testpassword"},
    )
    response = client.post(
        "/login",
        json={"username": "testuser2", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.cookies

def test_login_wrong_password():
    client.post(
        "/register",
        json={"username": "testuser3", "password": "testpassword"},
    )
    response = client.post(
        "/login",
        json={"username": "testuser3", "password": "wrongpassword"},
    )
    assert response.status_code == 404

def test_translate_no_cookie():
    response = client.post(
        "/translate",
        json={"text": "Hello", "direction": "en-fr"},
    )
    assert response.status_code == 401

def test_translate_success(monkeypatch):
    # Mock HF API
    def mock_translate(*args, **kwargs):
        return "Bonjour"
    
    monkeypatch.setattr(hf_client, "translate_text", mock_translate)

    # Login first
    client.post(
        "/register",
        json={"username": "testuser4", "password": "testpassword"},
    )
    login_response = client.post(
        "/login",
        json={"username": "testuser4", "password": "testpassword"},
    )
    
    response = client.post(
        "/translate",
        json={"text": "Hello", "direction": "en-fr"},
        cookies=login_response.cookies
    )
    assert response.status_code == 200
    assert response.json()["translation"] == "Bonjour"
