from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database.db import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to SkillSwap API!"}

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "username": "johndoe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "bio": "Python developer & teacher",
            "is_active": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "johndoe"
    assert "id" in data

def test_create_skill():
    response = client.post(
        "/skills/",
        json={
            "name": "Python Basics",
            "description": "Learn syntax and basic structures",
            "owner": "John Doe",
            "category": "Software Engineering",
            "level": "Beginner",
            "can_teach": True,
            "want_learn": False
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Python Basics"
    assert data["can_teach"] is True

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0