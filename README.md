# 🚀 taskflow-api

> A production-grade Task Management REST API built with **FastAPI**, **Async SQLAlchemy**, **Pydantic v2**, and **JWT Authentication** — demonstrating industry-standard Python backend engineering practices.

---

## 📌 Project Overview

| Field        | Detail                                               |
|--------------|------------------------------------------------------|
| **Repo Name**    | `taskflow-api`                                   |
| **Language**     | Python 3.11+                                     |
| **Framework**    | FastAPI                                          |
| **ORM**          | SQLAlchemy 2.0 (Async)                           |
| **Database**     | PostgreSQL (via `asyncpg` driver)                |
| **Auth**         | JWT (Access Token + Refresh Token)               |
| **Validation**   | Pydantic v2                                      |
| **Migrations**   | Alembic                                          |
| **Target**       | Complete in 7 days                               |

---

## 🎯 What You Will Build

A fully async, authenticated Task Management API where:

- **Users** can register, log in, manage their own profile
- **Tasks** can be created, listed, updated, deleted — scoped per user
- **Categories** can be created by users to organise tasks
- **Admins** have elevated access to manage all users and tasks
- Every route has proper HTTP status codes, error responses, and auth guards
- The entire server is **non-blocking** using `async/await` throughout

This project deliberately touches every concept you studied:

| Concept         | Where It Is Used                                                  |
|-----------------|-------------------------------------------------------------------|
| `AsyncIO`       | All DB calls, route handlers, service methods                    |
| `Pydantic v2`   | Request schemas, response schemas, config, validators, serialization |
| `SQLAlchemy 2`  | Async ORM models, relationships, query patterns                  |
| `FastAPI`       | Routing, dependency injection, lifespan, exception handlers      |
| JWT Auth        | Login, token refresh, route-level guards, role-based access      |

---

## 🗂️ Folder Structure

```
taskflow-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # App entry point — creates FastAPI instance, registers routers, lifespan
│   ├── config.py                # Pydantic BaseSettings — loads all env vars (.env)
│   ├── dependencies.py          # Shared FastAPI Depends() — get_db, get_current_user, require_admin
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py        # Master v1 router — includes all sub-routers with prefixes
│   │       ├── auth.py          # Auth routes: /register, /login, /refresh, /logout
│   │       ├── users.py         # User routes: /me, /me PATCH, admin user management
│   │       ├── tasks.py         # Task CRUD routes
│   │       └── categories.py    # Category CRUD routes
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py          # JWT creation/decoding, password hashing (bcrypt via passlib)
│   │   └── exceptions.py        # Custom exception classes + global exception handlers
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py              # DeclarativeBase — all models import from here
│   │   └── session.py           # Async engine + AsyncSessionLocal factory
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User SQLAlchemy model (id, email, hashed_password, role, timestamps)
│   │   ├── task.py              # Task model (id, title, description, status, priority, owner_id, category_id)
│   │   └── category.py          # Category model (id, name, owner_id)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py            # Shared Pydantic types: PaginatedResponse[T], MessageResponse
│   │   ├── auth.py              # LoginRequest, TokenResponse, RefreshRequest
│   │   ├── user.py              # UserCreate, UserRead, UserUpdate, UserPublic
│   │   ├── task.py              # TaskCreate, TaskRead, TaskUpdate, TaskPatch, TaskFilter
│   │   └── category.py          # CategoryCreate, CategoryRead, CategoryUpdate
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py      # Business logic: register user, authenticate, issue tokens, revoke tokens
│   │   ├── user_service.py      # Business logic: get profile, update profile, admin ops
│   │   ├── task_service.py      # Business logic: CRUD + ownership checks + filtering
│   │   └── category_service.py  # Business logic: CRUD + ownership checks
│   │
│   └── repositories/
│       ├── __init__.py
│       ├── base.py              # Generic async CRUD repository (get, get_multi, create, update, delete)
│       ├── user_repo.py         # User-specific queries: get_by_email, etc.
│       ├── task_repo.py         # Task-specific queries: filter by status, priority, category
│       └── category_repo.py     # Category-specific queries
│
├── alembic/
│   ├── env.py                   # Async-compatible Alembic env config — imports your models
│   └── versions/                # Auto-generated migration files live here
│
├── tests/
│   ├── conftest.py              # Pytest fixtures — async test client, DB override, test user factory
│   ├── test_auth.py             # Register, login, refresh, invalid credentials
│   ├── test_tasks.py            # Full CRUD + ownership + role access
│   └── test_users.py            # Profile ops + admin ops
│
├── .env.example                 # Template for environment variables — commit this, NOT .env
├── .gitignore
├── alembic.ini                  # Alembic config — points to your DB URL
├── requirements.txt             # Pinned dependencies
├── pyproject.toml               # Project metadata + tool configs (ruff, mypy)
└── README.md
```

---

## 📦 Dependencies

```txt
# requirements.txt

fastapi==0.115.0
uvicorn[standard]==0.30.0        # ASGI server — [standard] adds websocket + reload support
sqlalchemy==2.0.36               # SQLAlchemy 2.0 — async-first ORM
asyncpg==0.29.0                  # Async PostgreSQL driver
alembic==1.13.0                  # DB migrations
pydantic==2.9.0                  # Data validation — v2 is a full rewrite, much faster
pydantic-settings==2.5.0         # BaseSettings for .env loading
passlib[bcrypt]==1.7.4           # Password hashing
python-jose[cryptography]==3.3.0 # JWT encode/decode
python-multipart==0.0.12         # Required for form data (OAuth2 password flow)
httpx==0.27.0                    # Async HTTP client — used in tests

# Dev dependencies
pytest==8.3.0
pytest-asyncio==0.24.0
ruff==0.7.0                      # Linter + formatter (replaces black + isort + flake8)
mypy==1.12.0
```

---

## ⚙️ Environment Variables

```bash
# .env.example — copy to .env and fill in

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/taskflow_db

SECRET_KEY=your-super-secret-key-min-32-chars        # openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

APP_ENV=development
DEBUG=true
```

> **Why `pydantic-settings`?** Your `config.py` will use `BaseSettings` which auto-reads `.env` and validates types — so `DEBUG` becomes a proper Python `bool`, not a string. This is the standard FastAPI config pattern.

---

## 🛣️ All API Routes

Base path: `/api/v1`

### 🔐 Auth — `/auth`

| Method | Path              | Auth Required | Description                                      |
|--------|-------------------|:-------------:|--------------------------------------------------|
| POST   | `/auth/register`  | ❌            | Register a new user. Returns user + access token |
| POST   | `/auth/login`     | ❌            | Login. Returns access token + refresh token      |
| POST   | `/auth/refresh`   | ❌ (refresh token in body) | Exchange refresh token for new access token |
| POST   | `/auth/logout`    | ✅ User       | Revoke refresh token (server-side blacklist)     |

### 👤 Users — `/users`

| Method | Path                        | Auth Required   | Description                                       |
|--------|-----------------------------|:---------------:|---------------------------------------------------|
| GET    | `/users/me`                 | ✅ User         | Get current user's profile                        |
| PATCH  | `/users/me`                 | ✅ User         | Update own profile (name, password)               |
| DELETE | `/users/me`                 | ✅ User         | Delete own account                                |
| GET    | `/users`                    | ✅ Admin only   | List all users (paginated)                        |
| GET    | `/users/{user_id}`          | ✅ Admin only   | Get any user by ID                                |
| PATCH  | `/users/{user_id}/role`     | ✅ Admin only   | Promote/demote user role                          |
| DELETE | `/users/{user_id}`          | ✅ Admin only   | Hard delete a user                                |

### ✅ Tasks — `/tasks`

| Method | Path                | Auth Required | Description                                                         |
|--------|---------------------|:-------------:|---------------------------------------------------------------------|
| GET    | `/tasks`            | ✅ User       | Get all **own** tasks. Admins get all tasks. Supports query filters |
| POST   | `/tasks`            | ✅ User       | Create a new task                                                   |
| GET    | `/tasks/{task_id}`  | ✅ User       | Get one task by ID — enforces ownership                             |
| PUT    | `/tasks/{task_id}`  | ✅ User       | Full update — replaces entire task                                  |
| PATCH  | `/tasks/{task_id}`  | ✅ User       | Partial update — update only provided fields                        |
| DELETE | `/tasks/{task_id}`  | ✅ User       | Delete a task — enforces ownership                                  |

**Query Parameters for GET /tasks:**
```
?status=todo|in_progress|done
?priority=low|medium|high
?category_id=<uuid>
?page=1&limit=20
?sort_by=created_at&order=desc
```

### 🏷️ Categories — `/categories`

| Method | Path                      | Auth Required | Description                                |
|--------|---------------------------|:-------------:|--------------------------------------------|
| GET    | `/categories`             | ✅ User       | Get all own categories                     |
| POST   | `/categories`             | ✅ User       | Create a category                          |
| GET    | `/categories/{cat_id}`    | ✅ User       | Get one category                           |
| PUT    | `/categories/{cat_id}`    | ✅ User       | Update category name                       |
| DELETE | `/categories/{cat_id}`    | ✅ User       | Delete category (tasks become uncategorised)|

---

## 🗄️ Database Models

### `User`
```python
id: UUID (PK)
email: str (unique, indexed)
hashed_password: str
full_name: str
role: Enum("user", "admin")  # default: "user"
is_active: bool              # default: True
created_at: datetime
updated_at: datetime
```

### `Task`
```python
id: UUID (PK)
title: str
description: str | None
status: Enum("todo", "in_progress", "done")   # default: "todo"
priority: Enum("low", "medium", "high")        # default: "medium"
due_date: datetime | None
owner_id: UUID (FK → User.id)
category_id: UUID | None (FK → Category.id)
created_at: datetime
updated_at: datetime
```

### `Category`
```python
id: UUID (PK)
name: str
owner_id: UUID (FK → User.id)
created_at: datetime
```

---

## 🧱 Architecture: The Layer Flow

Understanding **why** the code is split this way is more important than memorising it.

```
HTTP Request
    ↓
Router (api/v1/tasks.py)
    → validates raw input with Pydantic schema
    → calls Depends() for DB session + current user
    ↓
Service (services/task_service.py)
    → enforces business rules (ownership, limits, etc.)
    → calls repository methods
    ↓
Repository (repositories/task_repo.py)
    → runs SQLAlchemy async queries
    → returns ORM model instances
    ↓
Database (PostgreSQL via asyncpg)
    ↑
ORM Model → Pydantic Schema → JSON Response
```

**Why this separation?**
- **Router** only knows HTTP — status codes, request/response shapes
- **Service** only knows business rules — "can this user do this?"
- **Repository** only knows SQL — no business logic, just queries
- This makes each layer independently testable and replaceable

> **Node.js parallel:** This is your Controller → Service → Repository pattern that you already know from NestJS/Express apps. Same idea, Python syntax.

---

## 🔐 Auth Deep Dive

### How JWT Works Here

```
1. POST /auth/login
   → verify password (bcrypt)
   → create access_token (short-lived: 30 min, JWT signed with SECRET_KEY)
   → create refresh_token (long-lived: 7 days, stored in DB)
   → return both tokens

2. Authenticated request
   → client sends: Authorization: Bearer <access_token>
   → get_current_user() dependency decodes JWT
   → extracts user_id from payload
   → loads user from DB
   → injects into route handler

3. POST /auth/refresh
   → client sends refresh_token in body
   → verify it exists in DB and is not expired/revoked
   → issue new access_token (and optionally new refresh_token)

4. POST /auth/logout
   → delete/revoke refresh_token from DB
```

### Dependency Chain

```python
# dependencies.py — this is core FastAPI pattern

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    # decode JWT, load user from DB

async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```

> **What's `Depends()`?** This is FastAPI's dependency injection — it's how you share DB sessions, auth checks, and anything else across routes without repeating yourself. It's the single most important FastAPI concept to internalise.

---

## 📐 Pydantic v2 — Advanced Usage Map

You will use these v2 features — not just basic `BaseModel`:

```python
from pydantic import BaseModel, field_validator, model_validator, computed_field
from pydantic import ConfigDict, Field, EmailStr

# 1. Model config (replaces v1 class Config)
class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # allows ORM → Pydantic conversion

# 2. Field validators
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    due_date: datetime | None = None

    @field_validator("due_date")
    @classmethod
    def due_date_must_be_future(cls, v):
        if v and v < datetime.utcnow():
            raise ValueError("due_date must be in the future")
        return v

# 3. Model validator (cross-field validation)
class PasswordChange(BaseModel):
    new_password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_must_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

# 4. Computed fields
class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    status: str
    due_date: datetime | None

    @computed_field
    @property
    def is_overdue(self) -> bool:
        return self.due_date is not None and self.due_date < datetime.utcnow()

# 5. Generic paginated response (reused across all list endpoints)
from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int
    pages: int
```

---

## ⚡ AsyncIO — What It Means in Practice

Every function that touches the database **must be `async def`** and use `await`:

```python
# ❌ Sync (blocks the event loop — kills concurrency)
def get_task(task_id: UUID, db: Session) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()

# ✅ Async (non-blocking — other requests proceed while this awaits)
async def get_task(task_id: UUID, db: AsyncSession) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()
```

**SQLAlchemy 2.0 Async pattern you'll use everywhere:**

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# SELECT
result = await db.execute(select(Task).where(Task.owner_id == user_id))
tasks = result.scalars().all()

# INSERT
db.add(new_task)
await db.commit()
await db.refresh(new_task)

# UPDATE
task.status = "done"
await db.commit()

# DELETE
await db.delete(task)
await db.commit()
```

> **Why `scalars()`?** `execute()` returns rows. `.scalars()` unwraps them to ORM objects. `.all()` gives you a list. `.first()` gives you one or None. `.scalar_one_or_none()` is a shorthand for single-object queries.

---

## 📁 File-by-File Build Guide

Build in this order. Each step is independently runnable and testable.

### Day 1 — Foundation

**`app/config.py`**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DEBUG: bool = False

    model_config = {"env_file": ".env"}

settings = Settings()
```

**`app/db/session.py`**
- Create async SQLAlchemy engine with `create_async_engine(settings.DATABASE_URL)`
- Create `AsyncSessionLocal` with `async_sessionmaker`
- Expose `get_db()` generator for `Depends()`

**`app/db/base.py`**
- Define `Base = DeclarativeBase()` — all models inherit from this
- Import all models here so Alembic can detect them for migrations

**`app/main.py`**
- Create `FastAPI()` instance with `lifespan` context manager
- Include the v1 router
- Register global exception handlers

**`app/core/exceptions.py`**
- Define `NotFoundException`, `ForbiddenException`, `ConflictException`
- Register `@app.exception_handler` for each — return consistent JSON error shapes

---

### Day 2 — Models + Migrations

**`app/models/user.py`**, **`app/models/task.py`**, **`app/models/category.py`**
- Define SQLAlchemy ORM models using the new 2.0 `Mapped[type]` annotation style
- Set up relationships: `User` has many `Task` and `Category`
- Use `mapped_column(default=uuid.uuid4)` for UUID PKs

**Alembic setup:**
```bash
alembic init alembic
# Edit alembic/env.py to use your async engine and import Base
alembic revision --autogenerate -m "initial_tables"
alembic upgrade head
```

---

### Day 3 — Auth

**`app/core/security.py`**
- `hash_password(plain: str) -> str` — uses `passlib` bcrypt
- `verify_password(plain: str, hashed: str) -> bool`
- `create_access_token(data: dict) -> str` — signs JWT with `python-jose`
- `create_refresh_token(user_id: UUID) -> str`
- `decode_token(token: str) -> dict` — raises if expired or invalid

**`app/schemas/auth.py`**
```python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
```

**`app/services/auth_service.py`**
- `register_user(data, db)` — check email uniqueness, hash password, insert user
- `authenticate_user(email, password, db)` — verify credentials
- `issue_tokens(user_id, db)` — create and persist refresh token

**`app/api/v1/auth.py`**
- Wire up all four auth routes using the service layer
- Return proper HTTP status codes: 201 Created, 200 OK, 401 Unauthorized

**`app/dependencies.py`**
- Implement `get_current_user()` and `require_admin()` here
- Test with: `GET /users/me` — should return 401 without token, 200 with valid token

---

### Day 4 — Users

**`app/schemas/user.py`**
```python
class UserCreate(BaseModel):         # POST /register — includes password
class UserRead(BaseModel):           # GET /users/me — no password field
class UserUpdate(BaseModel):         # PATCH /users/me — all fields optional
class UserPublic(BaseModel):         # Admin list view — minimal fields
```

**`app/repositories/user_repo.py`**
- `get_by_id(user_id, db)`
- `get_by_email(email, db)`
- `get_all(skip, limit, db)`
- `update(user, update_data, db)`

**`app/services/user_service.py`**
- `get_profile(current_user)`
- `update_profile(current_user, update_data, db)`
- `delete_account(current_user, db)`
- `admin_list_users(db, page, limit)`

**`app/api/v1/users.py`**
- Use `Depends(get_current_user)` for user routes
- Use `Depends(require_admin)` for admin routes

---

### Day 5 — Tasks

**`app/schemas/task.py`**
- `TaskCreate` — required fields with validators
- `TaskRead` — includes `is_overdue` computed field, serialises category
- `TaskUpdate` — all fields required (PUT semantics)
- `TaskPatch` — all fields optional (PATCH semantics) using `model_fields_set`
- `TaskFilter` — query param schema with `Optional` fields

**`app/repositories/task_repo.py`**
- Generic `get_multi` that accepts filter kwargs
- Build dynamic `WHERE` clauses using SQLAlchemy `select().where()`

**`app/services/task_service.py`**
- Every mutation checks: `if task.owner_id != current_user.id and current_user.role != "admin": raise ForbiddenException`

**`app/api/v1/tasks.py`**
- Full CRUD routes
- GET `/tasks` — uses `Annotated[TaskFilter, Query()]` for type-safe query params

---

### Day 6 — Categories + Polish

**Categories** — same pattern as Tasks but simpler (no status/priority)

**Polish:**
- Add `updated_at` auto-update via SQLAlchemy `onupdate=func.now()`
- Add request logging middleware
- Ensure all routes return correct status codes:
  - `201 Created` on POST
  - `204 No Content` on DELETE
  - `404 Not Found` with message on missing resource
  - `409 Conflict` on duplicate email
  - `422 Unprocessable Entity` on validation failure (FastAPI auto-handles this)

---

### Day 7 — Tests + Cleanup

**`tests/conftest.py`**
```python
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def test_user(db_session):
    # create a user and return with credentials
```

**Write tests for:**
- Register + login flow
- Auth guard — unauthenticated requests return 401
- Ownership guard — user A cannot delete user B's task (expect 403)
- Admin access — admin can list all tasks, regular user cannot
- Pagination — GET /tasks?page=2&limit=5 returns correct slice

---

## 🔑 Key Concepts to Look Up in the Docs (Not Tutorials)

When you get stuck, go straight to the source — these are the exact doc pages you will need:

| Topic | Doc URL |
|-------|---------|
| FastAPI Dependency Injection | https://fastapi.tiangolo.com/tutorial/dependencies/ |
| FastAPI OAuth2 + JWT | https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ |
| SQLAlchemy 2.0 Async | https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html |
| SQLAlchemy 2.0 ORM Mapped | https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html |
| Alembic with Async | https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic |
| Pydantic v2 Validators | https://docs.pydantic.dev/latest/concepts/validators/ |
| Pydantic v2 Configuration | https://docs.pydantic.dev/latest/concepts/config/ |
| Pydantic v2 Generic Models | https://docs.pydantic.dev/latest/concepts/pydantic_concepts/#generic-models |
| FastAPI Background Tasks | https://fastapi.tiangolo.com/tutorial/background-tasks/ |
| FastAPI Middleware | https://fastapi.tiangolo.com/tutorial/middleware/ |
| pytest-asyncio | https://pytest-asyncio.readthedocs.io/en/latest/ |

---

## 🚦 HTTP Status Code Reference

Use these consistently — don't just return 200 for everything:

| Scenario                     | Code | Reason                        |
|------------------------------|------|-------------------------------|
| Resource created             | 201  | POST success                  |
| Delete success               | 204  | No content to return          |
| Bad request body             | 400  | Malformed data                |
| Not authenticated            | 401  | Missing/invalid token         |
| Authenticated, not allowed   | 403  | Valid token, wrong role/ownership |
| Resource not found           | 404  | DB lookup returned None       |
| Duplicate (e.g. email)       | 409  | Conflict with existing data   |
| Validation error             | 422  | Pydantic rejects the body     |
| Server error                 | 500  | Unhandled exception           |

---

## 📋 Daily Checklist

```
Day 1 ☐  Config + DB session + main.py + exceptions + server starts on uvicorn
Day 2 ☐  All 3 models + Alembic migration runs + tables created in PG
Day 3 ☐  Register + Login working + /users/me returns 401 without token
Day 4 ☐  Full users routes — profile, update, admin list
Day 5 ☐  Full task CRUD — all filters + ownership guards working
Day 6 ☐  Categories done + all status codes correct + clean error responses
Day 7 ☐  Tests written + all pass + README reviewed + push to GitHub
```

---

## 🧠 Things That Will Confuse You (Pre-Warnings)

**1. SQLAlchemy async sessions are NOT thread-safe — always use `Depends(get_db)`**
Never create a session manually inside a route. Always inject it. The `yield` in `get_db()` ensures the session is closed after the request, even on errors.

**2. `await db.refresh(obj)` after commit**
After `await db.commit()`, your ORM object's attributes are expired. Call `await db.refresh(obj)` to reload them from the DB before returning the response.

**3. Alembic env.py needs async setup**
The standard Alembic `env.py` is sync. You'll need to modify it to use `run_async_migrations()` with `asyncio.run()`. The Alembic async cookbook (linked above) shows exactly how.

**4. Pydantic v2 `from_attributes=True` is required for ORM → Schema conversion**
Without `model_config = ConfigDict(from_attributes=True)`, Pydantic won't know how to read SQLAlchemy ORM objects. Every "Read" schema needs this.

**5. `select()` vs `.query()` — use `select()`**
SQLAlchemy 2.0 deprecated the old `.query()` API. Always use `select(Model).where(...)` and `await db.execute(...)`.

**6. JWT decode errors → 401, not 500**
Wrap `jose.decode()` in a try/except and raise `HTTPException(status_code=401)` on `JWTError`. If you don't, expired tokens crash your server.

---

## 🚀 Running the Project

```bash
# Clone and setup
git clone https://github.com/your-username/taskflow-api
cd taskflow-api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Fill in DATABASE_URL and SECRET_KEY

# Migrate
alembic upgrade head

# Run (FastAPI CLI via uv)
uv run fastapi dev app/main.py

# Interactive API docs available at:
# http://localhost:8000/docs   (Swagger UI)
# http://localhost:8000/redoc  (ReDoc)
```

```bash
# Run tests
pytest tests/ -v --asyncio-mode=auto
```

---

## 🏁 Definition of Done

The project is complete when:

- [ ] All routes in this README are implemented and return correct status codes
- [ ] Unauthenticated requests to protected routes return `401`
- [ ] Cross-user resource access returns `403`
- [ ] Task filtering by status/priority/category works correctly
- [ ] Pagination works on all list endpoints
- [ ] Alembic manages the schema (no `Base.metadata.create_all()` in production code)
- [ ] All Pydantic schemas use `from_attributes=True` where needed
- [ ] No `db.query()` calls — only `select()` / `await db.execute()`
- [ ] Auth tests, task ownership tests, and admin access tests pass
- [ ] Server handles errors gracefully — no unhandled 500s for expected failures

---

*Built as part of backend engineering learning track — FastAPI / Python / Async stack.*
