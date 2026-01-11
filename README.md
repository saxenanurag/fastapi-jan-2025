# FastAPI January 2025 Presentation & Code Example

This repository contains the materials for the Cleveland Python Meetup presentation on FastAPI, held in January 2025. It includes a sample FastAPI application and the presentation slides.

## Project Structure

- **`code_example/`**: A complete, working FastAPI application demonstrating CRUD operations with SQLModel.
- **`slides/`**: The Markdown source for the presentation slides (`fastapi_presentation.md`).

## Code Example: Ingredients API

The `code_example` directory contains a simple API for managing a database of ingredients. It demonstrates core FastAPI features including:
-   Pydantic models for data validation (Input/Output schemas).
-   SQLModel for ORM (SQLite database).
-   Dependency Injection for database sessions.
-   CRUD endpoints (Create, Read, Update, Delete).

### Prerequisites

-   Python 3.14+
-   `uv` (recommended for package management)

### Setup & Running

1.  Navigate to the `code_example` directory:
    ```bash
    cd code_example
    ```

2.  Install dependencies using `uv`:
    ```bash
    uv sync
    ```

3.  Run the application:
    ```bash
    uv run uvicorn main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.

4.  Explore the interactive documentation:
    -   Swagger UI: `http://127.0.0.1:8000/docs`
    -   ReDoc: `http://127.0.0.1:8000/redoc`

### Running Tests

To run the tests using `pytest`:

```bash
uv run pytest
```

## Presentation

The presentation covers:
-   Introduction to FastAPI.
-   Comparison with Django and Flask.
-   Key features (Performance, Async, Type Hints, etc.).
-   Best practices.

You can view the raw markdown in `slides/fastapi_presentation.md`.
