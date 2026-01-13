import pytest
from fastapi.testclient import TestClient
from main import app, get_session
from models import Ingredient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


@pytest.fixture(name="session")
def session_fixture():
    """
    Pytest fixture to create a fresh in-memory database session for each test.

    - Uses 'sqlite://' for an in-memory database.
    - StaticPool is used because in-memory SQLite is thread-sensitive.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Pytest fixture to create a TestClient with the database session overridden.

    - app.dependency_overrides allows us to swap the real get_session dependency
      with a lambda that returns our test session.
    - This ensures tests run against the in-memory database, not the real one.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_ingredient(client: TestClient):
    """
    Test the create ingredient endpoint.
    """
    response = client.post(
        "/ingredients/",
        json={"name": "Test Bun", "category": "Bread", "quantity": 10},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Test Bun"
    assert data["category"] == "Bread"
    assert data["quantity"] == 10
    assert data["id"] is not None


def test_read_ingredients(client: TestClient):
    """
    Test reading a list of ingredients.
    """
    # Create some data first
    client.post(
        "/ingredients/",
        json={"name": "Test Bun", "category": "Bread", "quantity": 10},
    )
    client.post(
        "/ingredients/",
        json={"name": "Test Sausage", "category": "Meat", "quantity": 5},
    )

    response = client.get("/ingredients/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == "Test Bun"
    assert data[1]["name"] == "Test Sausage"


def test_read_ingredient(client: TestClient):
    """
    Test reading a single ingredient by ID.
    """
    response = client.post(
        "/ingredients/",
        json={
            "name": "Unique Ingredient",
            "category": "Special",
            "quantity": 1,
        },
    )
    ingredient_id = response.json()["id"]

    response = client.get(f"/ingredients/{ingredient_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Unique Ingredient"
    assert data["id"] == ingredient_id


def test_update_ingredient(client: TestClient):
    """
    Test updating an ingredient.
    """
    response = client.post(
        "/ingredients/",
        json={"name": "Old Name", "category": "Old Cat", "quantity": 1},
    )
    ingredient_id = response.json()["id"]

    # Partial update: only name and quantity
    response = client.patch(
        f"/ingredients/{ingredient_id}",
        json={"name": "New Name", "quantity": 5},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "New Name"
    assert data["quantity"] == 5
    assert data["category"] == "Old Cat"  # Should remain unchanged


def test_delete_ingredient(client: TestClient):
    """
    Test deleting an ingredient.
    """
    response = client.post(
        "/ingredients/",
        json={"name": "To Delete", "category": "Trash", "quantity": 1},
    )
    ingredient_id = response.json()["id"]

    response = client.delete(f"/ingredients/{ingredient_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

    # Verify it's gone
    response = client.get(f"/ingredients/{ingredient_id}")
    assert response.status_code == 404
