---
marp: true
theme: default
paginate: true
backgroundColor: #fff
header: 'Cleveland Python Meetup January 2025'
footer: 'Jan 13, 2026'
style: |
  section.lead {
    text-align: center;
    justify-content: center;
  }
---

<!-- _class: lead -->

# FastAPI
## Building High-Performance APIs with Modern Python


Anurag Saxena

Clepy and ClePyLadies
Jan 2026

---

# Agenda

1. Introduction to FastAPI
2. Framework Comparison: FastAPI vs. Django vs. Flask
3. Deep Dive into Key Features
4. Best Practices
5. Conclusion

---

# Introduction
## What is FastAPI?

> "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints."

- **Modern**: Built on recent standards (Python 3.6+, OpenAPI, JSON Schema).
- **Fast**: Comparable to NodeJS and Go (thanks to Starlette and Pydantic).
- **Typed**: Heavy use of Python Type Hints for validation and documentation.

---

# Comparing FastAPI vs. Django vs. Flask

| Feature | FastAPI | Django | Flask |
| :--- | :--- | :--- | :--- |
| **Type** | Micro-framework (Async) | Monolithic "Batteries Included" | Micro-framework (Sync) |
| **Server Side Rendering** | No | Yes | Yes (using Jinja Templates) |
| **Performance** | Very High (ASGI) | Good (WSGI, heavier) | Good (WSGI) |
| **Async** | First-class | Added later (Partial) | Via extensions/Quart |
| **Validation** | Pydantic | Forms / DRF | Extensions (Marshmallow) |

---
# Comparing FastAPI vs. Django vs. Flask

| Feature | FastAPI | Django | Flask |
| :--- | :--- | :--- | :--- |
| **Docs** | Automatic | Extensions (drf-yasg) | Extensions (Flask-RESTX) |

---

# Comparison: Performance

- **FastAPI**:
  - Built on **Starlette** (web parts) and **Pydantic** (data parts).
  - Uses **ASGI** (Asynchronous Server Gateway Interface).
  - One of the fastest Python frameworks available.

- **Django/Flask**:
  - Traditionally **WSGI** (Web Server Gateway Interface).
  - Synchronous by default (blocking I/O).
  - *Django* has overhead due to its massive feature set.
  - *Flask* is lighter but still limited by WSGI in standard usage.

---

# Comparison: Developer Experience (DX)

- **FastAPI**:
  - **Autocompletion**: Editors "understand" your data models; catches typos instantly.
  - **Type Checks**: Catch errors at edit time, not runtime.
  - **Less Boilerplate**: Types define validation and schema simultaneously.

---

# Comparison: Developer Experience (DX)

- **Django**:
  - Excellent for standard CRUD apps.
  - "Magic" can sometimes obscure flow.
  - Context switching between Python and Django-specific DSLs (ORMs, Templates).

- **Flask**:
  - Simple start, but you must choose your own libraries (DB, Auth, Validation).
  - Can lead to "decision fatigue" or disparate patterns across projects.

---

# FastAPI features

---

# Feature 1: High Performance

**Speed Matters.**

- **Tech Stack**:
    - **Starlette**: For the web routing and request handling.
    - **Pydantic**: For data validation.
    - **Uvicorn**: The ASGI server (lightning fast).
- **Why?**: Async I/O handles thousands of concurrent connections (Wait-free I/O).

---

# Under the Hood: The Power Trio

**FastAPI stands on the shoulders of giants.**

1.  **Starlette (The Web)**:
    - Provides the web micro-framework capabilities.
    - Handles routing, WebSockets, and ASGI support.
    - *FastAPI is a class that inherits from Starlette.*

2.  **Pydantic (The Data)**:
    - Provides data validation and settings management using Python type hints.
    - Extremely fast (core written in Rust in V2).
    - *FastAPI uses it to validate requests and responses.*

---

3.  **Uvicorn (The Server)**:
    - An ASGI web server implementation.
    - Runs your FastAPI application.
    - *FastAPI is the application; Uvicorn is the runner.*

---


# Feature 2: Automatic Documentation

**No more stale docs.**

- Based on **OpenAPI** (formerly Swagger).
- **Interactive UIs** generated automatically from code:
    1. **Swagger UI**: Call your API directly from the browser.
    2. **ReDoc**: Clean, readable documentation reference.
- **Zero Config**: Just define your routes and types, FastAPI does the rest.

---

# Feature 3: Type Hints & Pydantic

**Python types are powerful.**

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

app = FastAPI()

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

---

- **Validation**: `item_id` MUST be an `int`. `item` payload matches `Item` schema.
- **Conversion**: Automatically parses JSON body to Python objects.
- **Editor Support**: You get dot-completion on `item.name`.

---

# Feature 4: Dependency Injection

**Clean, modular, and testable code.**

- **Built-in System**: No external libraries needed.
- **Usage**:
    - Shared logic (database connections, auth users).
    - Security requirements.
- **Hierarchical**: Dependencies can have dependencies.

```python
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

---

# Feature 5: Async Support

**Modern Concurrency.**

- **`async` and `await`**: Native keywords in Python.
- **Non-blocking**: Database calls, external API requests don't freeze the server.
- **Simplicity**: You can mix `def` (sync) and `async def` endpoints. FastAPI runs sync functions in a threadpool automatically.

```python
@app.get("/")
async def read_results():
    results = await some_library.do_heavy_lifting()
    return results
```

---

# Feature 6: Security & Authentication

**Secure by default.**

- **OAuth2**: Built-in support for OAuth2 scopes and flows.
- **Utilities**: Helpers for API Keys, HTTP Basic, JWT tokens.
- **Integration**: Tightly coupled with the Dependency Injection system.
  - Simply depend on `get_current_user` in your route.
- **OpenAPI**: Security schemes are automatically added to the interactive docs (the "Authorize" button).
- Docs link: https://fastapi.tiangolo.com/tutorial/security/first-steps/

---

# Feature 7: Standards-Based

**Stand on the shoulders of giants.**

- **OpenAPI**: The API definition standard.
- **JSON Schema**: The data validation standard.
- **OAuth2**: The authentication standard.

**Benefit**:
- Client Code Generation (generate SDKs for frontend/mobile automatically).
- Tooling compatibility.

---

# Feature 8: Editor Support

**Your IDE is your best friend.**

- Because FastAPI is based on standard Python type hints, editors like VS Code and PyCharm understand it perfectly.
- **Benefits**:
    - Autocompletion for request data.
    - Type checking for response data.
    - Refactoring is safer and easier.
- **Result**: "Fewer Bugs" (claimed ~40% reduction).

---

# Feature 9: Background Tasks

**Fire and forget.**

- Handle operations *after* returning a response.
- Useful for:
    - Email notifications.
    - Data processing.
- Simple API

---

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as log:
        log.write(message)

@app.post("/send-notification/")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent"}
```

---

# Feature 10: WebSockets

**Real-time communication.**

- Full support for WebSockets.
- Easy to use dependency injection within WebSocket routes.
- Handles concurrent connections efficiently.

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

---

# Best Practices (1/2)
*From `zhanymkanov/fastapi-best-practices`*

1.  **Project Structure**:
    - Avoid flat structures. Modularize by domain (e.g., `src/auth`, `src/posts`).
    - Keep `main.py` simple.
2.  **Pydantic**:
    - Use Pydantic for validation, NOT your ORM.
    - Separate schemas for **Input** (Create/Update) and **Output** (Response) to avoid leaking internal data (like password hashes).

---

# Best Practices (2/2)

3.  **Dependencies**:
    - Use `Depends` for reusable logic (DB sessions, current user).
    - Don't hardcode logic inside route handlers.
4.  **Configuration**:
    - Use `pydantic-settings` to manage environment variables.
5.  **Testing**:
    - Use `TestClient` (wraps Starlette/Requests) or `AsyncClient` (httpx).
    - Test separate modules in isolation.

---

# Conclusion

**Why Choose FastAPI?**

1.  **Performance**: It's fast (latency and throughput).
2.  **Productivity**: You write less code, debug less, and ship faster.
3.  **Documentation**: Free, always up-to-date API docs.
4.  **Modern**: Learns from the past (Django/Flask) and adopts the future (Async/Types).

