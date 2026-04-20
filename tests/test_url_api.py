from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_urls.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_shorten_and_redirect_flow():
    create_response = client.post("/api/shorten", json={"original_url": "https://example.com"})
    assert create_response.status_code == 200
    short_url = create_response.json()["short_url"]
    code = short_url.split("/")[-1]

    redirect_response = client.get(f"/api/{code}", follow_redirects=False)
    assert redirect_response.status_code in (307, 302)
    assert redirect_response.headers["location"] == "https://example.com/"

    stats_response = client.get(f"/api/stats/{code}")
    assert stats_response.status_code == 200
    assert stats_response.json()["clicks"] == 1


def test_custom_code_validation():
    response = client.post(
        "/api/custom",
        json={"original_url": "https://example.com", "custom_code": "bad code"},
    )
    assert response.status_code == 422


def test_custom_code_conflict():
    payload = {"original_url": "https://example.com", "custom_code": "mycode"}
    first = client.post("/api/custom", json=payload)
    assert first.status_code == 200

    second = client.post("/api/custom", json=payload)
    assert second.status_code == 400
    assert second.json()["detail"] == "Code already exists"
