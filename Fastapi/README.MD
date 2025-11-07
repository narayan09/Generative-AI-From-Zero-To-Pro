# FastAPI From Zero to Pro — Practical, Hands-On Series

A comprehensive, production-ready FastAPI curriculum focused on **day-to-day concepts**, **hands-on mini-projects**, and **real-world patterns**. Each module is designed to be completed in 2–3 hours with runnable code and clear examples.

Learn FastAPI essentials in **7 days** with minimal theory and maximum hands-on practice. Perfect for busy developers who want to build production-ready APIs quickly.

**Time Commitment**: ~2-3 hours per day | **Total**: 14-21 hours

---

## 📅 One-Week Learning Plan

| Day | Topic | Time | Mini-Project |
|-----|-------|------|--------------|
| **Day 1** | Setup & Basics + HTTP Methods | 2.5h | Hello API with GET/POST/PUT/DELETE |
| **Day 2** | Routing & Path/Query Parameters | 2.5h | Todo CRUD with filtering |
| **Day 3** | Pydantic Validation | 2.5h | Form validation with error handling |
| **Day 4** | Dependencies & Auth | 2.5h | Login + protected routes |
| **Day 5** | Database (SQLAlchemy) | 3h | Persistent Todo app |
| **Day 6** | Async, Logging, Settings | 2.5h | Async API + config management |
| **Day 7** | Testing + Final Project | 3h | Full test suite + capstone project |

---

## 🎯 Day 1: Setup, Basics & HTTP Methods (2.5 hours)

### What You'll Learn
- FastAPI project structure
- Running with uvicorn
- GET, POST, PUT, DELETE methods
- Status codes
- JSON responses

### Quick Concepts

**HTTP Methods Explained**:
- **GET** — Retrieve data (safe, idempotent)
- **POST** — Create new data
- **PUT** — Replace entire resource
- **DELETE** — Remove data

### Code Example: Hello API with All HTTP Methods

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FastAPI Week 1")

# Data model
class Item(BaseModel):
    id: int
    name: str
    price: float
    description: str = None

# In-memory storage
items_db = {}
next_id = 1

# GET - Retrieve all items
@app.get("/items", status_code=200)
async def get_all_items():
    return {"items": list(items_db.values())}

# GET - Retrieve single item by ID
@app.get("/items/{item_id}", status_code=200)
async def get_item(item_id: int):
    if item_id not in items_db:
        return {"error": "Item not found"}, 404
    return items_db[item_id]

# POST - Create new item
@app.post("/items", status_code=201)
async def create_item(item: Item):
    global next_id
    item_data = item.dict()
    item_data["id"] = next_id
    items_db[next_id] = item_data
    next_id += 1
    return {"message": "Item created", "item": item_data}

# PUT - Update entire item
@app.put("/items/{item_id}", status_code=200)
async def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        return {"error": "Item not found"}, 404
    item_data = item.dict()
    item_data["id"] = item_id
    items_db[item_id] = item_data
    return {"message": "Item updated", "item": item_data}

# DELETE - Remove item
@app.delete("/items/{item_id}", status_code=200)
async def delete_item(item_id: int):
    if item_id not in items_db:
        return {"error": "Item not found"}, 404
    deleted = items_db.pop(item_id)
    return {"message": "Item deleted", "item": deleted}

# Root endpoint
@app.get("/", status_code=200)
async def root():
    return {"message": "FastAPI Crash Course Day 1"}
```

### Setup Instructions

```bash
# Create project folder
mkdir fastapi-week && cd fastapi-week

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install FastAPI and uvicorn
pip install fastapi uvicorn[standard]

# Create main.py with code above
# Run server
uvicorn main:app --reload

# Test endpoints:
# GET    http://localhost:8000/items
# POST   http://localhost:8000/items (with JSON body)
# PUT    http://localhost:8000/items/1
# DELETE http://localhost:8000/items/1
```

### Mini-Project: Simple Item Store API

**Requirements**:
- ✅ Store items in memory (dictionary)
- ✅ GET all items
- ✅ GET single item by ID
- ✅ POST to create item (auto-increment ID)
- ✅ PUT to update item
- ✅ DELETE to remove item
- ✅ Return proper status codes (200, 201, 404)

**Test with curl/Postman**:
```bash
# Create item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "description": "Gaming laptop"}'

# Get all items
curl http://localhost:8000/items

# Update item
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "MacBook", "price": 1299.99}'

# Delete item
curl -X DELETE http://localhost:8000/items/1
```

### Day 1 Checklist
- [ ] Install FastAPI and uvicorn
- [ ] Create main.py with code above
- [ ] Run `uvicorn main:app --reload`
- [ ] Test all 5 endpoints in Swagger UI (/docs)
- [ ] Modify code to add status code 404 handling
- [ ] Push code to GitHub

---

## 🎯 Day 2: Routing & Parameters (2.5 hours)

### What You'll Learn
- Path parameters with type hints
- Query parameters with defaults and validation
- Optional parameters
- Pagination (skip/limit)
- Multiple path parameters

### Code Example: Todo CRUD with Filtering

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Todo App - Day 2")

class Todo(BaseModel):
    id: int = None
    title: str
    description: str = None
    completed: bool = False
    priority: int = 1  # 1-5

# Database
todos_db = {}
next_id = 1

# GET all todos with filtering
@app.get("/todos", response_model=List[Todo])
async def list_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    completed: Optional[bool] = None,
    priority: Optional[int] = Query(None, ge=1, le=5)
):
    """
    Get todos with pagination and optional filters
    - skip: number of items to skip (default: 0)
    - limit: max items to return (default: 10, max: 100)
    - completed: filter by completion status (optional)
    - priority: filter by priority level (optional)
    """
    result = list(todos_db.values())
    
    # Apply filters
    if completed is not None:
        result = [t for t in result if t["completed"] == completed]
    
    if priority is not None:
        result = [t for t in result if t["priority"] == priority]
    
    # Pagination
    return result[skip : skip + limit]

# GET single todo
@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[todo_id]

# POST create todo
@app.post("/todos", status_code=201, response_model=Todo)
async def create_todo(todo: Todo):
    """Create a new todo"""
    global next_id
    todo_data = todo.dict()
    todo_data["id"] = next_id
    todos_db[next_id] = todo_data
    next_id += 1
    return todo_data

# PUT update todo
@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo):
    """Update an existing todo"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_data = todo.dict()
    todo_data["id"] = todo_id
    todos_db[todo_id] = todo_data
    return todo_data

# DELETE todo
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    """Delete a todo"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_db[todo_id]

# PATCH - Mark todo as complete
@app.patch("/todos/{todo_id}/complete", response_model=Todo)
async def complete_todo(todo_id: int):
    """Mark a todo as complete"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos_db[todo_id]["completed"] = True
    return todos_db[todo_id]

# Search todos by title
@app.get("/todos/search/{search_term}", response_model=List[Todo])
async def search_todos(search_term: str):
    """Search todos by title"""
    return [t for t in todos_db.values() if search_term.lower() in t["title"].lower()]
```

### Usage Examples

```bash
# Create a todo
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Complete crash course", "priority": 5}'

# Get all todos
curl "http://localhost:8000/todos"

# Get with pagination
curl "http://localhost:8000/todos?skip=0&limit=5"

# Filter by completed status
curl "http://localhost:8000/todos?completed=false"

# Filter by priority
curl "http://localhost:8000/todos?priority=5"

# Get single todo
curl "http://localhost:8000/todos/1"

# Mark as complete
curl -X PATCH http://localhost:8000/todos/1/complete

# Search todos
curl "http://localhost:8000/todos/search/FastAPI"

# Delete todo
curl -X DELETE http://localhost:8000/todos/1
```

### Day 2 Checklist
- [ ] Implement list_todos with skip/limit
- [ ] Add completed filter
- [ ] Add priority filter
- [ ] Test all query parameter combinations
- [ ] Add search endpoint
- [ ] Test with Swagger UI
- [ ] Commit to GitHub

---

## 🎯 Day 3: Pydantic Validation (2.5 hours)

### What You'll Learn
- BaseModel and data validation
- Field constraints (min, max, regex, etc.)
- Custom validators
- Error handling
- Type hints and strict mode

### Code Example: User Signup with Validation

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
import re

app = FastAPI(title="User Validation - Day 3")

# User schema with validation
class User(BaseModel):
    id: int = None
    username: str = Field(..., min_length=3, max_length=20, regex="^[a-zA-Z0-9_]+$")
    email: EmailStr  # Requires: pip install pydantic[email]
    password: str = Field(..., min_length=8, description="Min 8 chars, 1 number, 1 uppercase")
    age: int = Field(..., ge=18, le=120, description="Must be 18-120")
    bio: Optional[str] = Field(None, max_length=500)
    
    # Custom validator
    @validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v
    
    @validator("username")
    def username_alphanumeric(cls, v):
        if not v.isalnum() and "_" not in v:
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    age: int

# Database
users_db = {}
next_id = 1

# POST - Signup with validation
@app.post("/signup", status_code=201, response_model=UserResponse)
async def signup(user: User):
    """
    Register new user with validation
    - Username: 3-20 chars, alphanumeric + underscores only
    - Email: valid email format
    - Password: min 8 chars, 1 uppercase, 1 number
    - Age: 18-120
    """
    # Check if user exists
    for existing_user in users_db.values():
        if existing_user["username"] == user.username:
            raise HTTPException(status_code=409, detail="Username already exists")
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=409, detail="Email already exists")
    
    global next_id
    user_data = user.dict()
    user_data["id"] = next_id
    # In real app: hash password!
    users_db[next_id] = user_data
    next_id += 1
    
    return user_data

# GET user profile
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user profile"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = users_db[user_id]
    return UserResponse(**user_data)

# PUT update profile
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: User):
    """Update user profile"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user.dict()
    user_data["id"] = user_id
    users_db[user_id] = user_data
    
    return user_data
```

### Usage Examples

```bash
# Valid signup
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "age": 25,
    "bio": "Developer and FastAPI enthusiast"
  }'

# Invalid: password too weak (no uppercase)
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_doe",
    "email": "jane@example.com",
    "password": "weakpass123",
    "age": 22
  }'

# Invalid: username too short
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ab",
    "email": "test@example.com",
    "password": "StrongPass123",
    "age": 30
  }'

# Invalid: age too young
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "young_user",
    "email": "young@example.com",
    "password": "StrongPass123",
    "age": 15
  }'
```

### Day 3 Checklist
- [ ] Install pydantic[email]: `pip install pydantic[email]`
- [ ] Create User model with Field constraints
- [ ] Add password validator (uppercase + number)
- [ ] Test invalid inputs in Swagger UI
- [ ] Verify error messages are helpful
- [ ] Test email format validation
- [ ] Commit to GitHub

---

## 🎯 Day 4: Dependencies & Authentication (2.5 hours)

### What You'll Learn
- Dependency Injection with Depends
- Reusable dependencies
- JWT tokens basics
- Protected routes
- Token validation

### Code Example: Login + Protected Routes

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import jwt
from typing import Optional

app = FastAPI(title="Auth - Day 4")

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security scheme
security = HTTPBearer()

# Models
class User(BaseModel):
    id: int = None
    username: str
    email: EmailStr

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    username: str

# Database
users_db = {
    1: {"id": 1, "username": "demo", "email": "demo@example.com", "password": "demo123"}
}

# Utility functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency: Get current user from token
async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    """Validate JWT token and return current user"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Find user
    for user in users_db.values():
        if user["username"] == username:
            return User(**user)
    
    raise HTTPException(status_code=401, detail="User not found")

# POST - Login endpoint
@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Login with username and password
    Returns JWT token for authenticated requests
    """
    # Find user
    user = None
    for u in users_db.values():
        if u["username"] == request.username and u["password"] == request.password:
            user = u
            break
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": User(**user)
    }

# GET - Protected route
@app.get("/profile", response_model=User)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile (protected route)"""
    return current_user

# POST - Create data (protected)
@app.post("/posts", status_code=201)
async def create_post(
    content: str,
    current_user: User = Depends(get_current_user)
):
    """Create a post (protected route)"""
    return {
        "id": 1,
        "author": current_user.username,
        "content": content,
        "created_at": datetime.utcnow()
    }

# GET - List user's posts (protected)
@app.get("/my-posts")
async def my_posts(current_user: User = Depends(get_current_user)):
    """Get current user's posts"""
    return {
        "user": current_user.username,
        "posts": [
            {"id": 1, "content": "First post"},
            {"id": 2, "content": "Second post"}
        ]
    }

# Public endpoint
@app.get("/health")
async def health():
    """Health check (no auth needed)"""
    return {"status": "ok"}
```

### Usage Examples

```bash
# Login to get token
TOKEN=$(curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo123"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo "Token: $TOKEN"

# Use token to access protected route
curl -X GET http://localhost:8000/profile \
  -H "Authorization: Bearer $TOKEN"

# Create post (protected)
curl -X POST http://localhost:8000/posts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "My first FastAPI post"}'

# Get my posts (protected)
curl -X GET http://localhost:8000/my-posts \
  -H "Authorization: Bearer $TOKEN"

# Try without token (will fail)
curl -X GET http://localhost:8000/profile
```

### Day 4 Checklist
- [ ] Install: `pip install pyjwt python-multipart`
- [ ] Install: `pip install pydantic[email]`
- [ ] Create login endpoint
- [ ] Implement JWT token creation
- [ ] Create get_current_user dependency
- [ ] Add protected routes
- [ ] Test with Swagger UI
- [ ] Test with invalid tokens
- [ ] Commit to GitHub

---

## 🎯 Day 5: Database with SQLAlchemy (3 hours)

### What You'll Learn
- SQLAlchemy ORM models
- Database sessions
- CRUD operations
- Migrations with Alembic
- Relationships

### Code Example: Persistent Todo App

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List

# Database setup
DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI(title="Todo DB - Day 5")

# SQLAlchemy Model
class TodoModel(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class TodoCreate(BaseModel):
    title: str
    description: str = None
    priority: int = 1

class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None
    priority: int = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool
    priority: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dependency: Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET all todos
@app.get("/todos", response_model=List[TodoResponse])
async def list_todos(
    skip: int = 0,
    limit: int = 10,
    completed: bool = None,
    db: Session = Depends(get_db)
):
    """Get todos with optional filters"""
    query = db.query(TodoModel)
    
    if completed is not None:
        query = query.filter(TodoModel.completed == completed)
    
    return query.offset(skip).limit(limit).all()

# GET single todo
@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo"""
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# POST create todo
@app.post("/todos", status_code=201, response_model=TodoResponse)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo"""
    db_todo = TodoModel(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# PUT update todo
@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db)
):
    """Update a todo"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# DELETE todo
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()

# PATCH mark complete
@app.patch("/todos/{todo_id}/complete", response_model=TodoResponse)
async def complete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Mark a todo as complete"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db_todo.completed = True
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# GET stats
@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get todo statistics"""
    total = db.query(TodoModel).count()
    completed = db.query(TodoModel).filter(TodoModel.completed == True).count()
    pending = total - completed
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": (completed / total * 100) if total > 0 else 0
    }
```

### Setup Instructions

```bash
# Install database dependencies
pip install sqlalchemy

# Run the app (tables created automatically)
uvicorn main:app --reload

# Test endpoints at http://localhost:8000/docs
```

### Day 5 Checklist
- [ ] Install sqlalchemy: `pip install sqlalchemy`
- [ ] Create TodoModel with SQLAlchemy
- [ ] Create SessionLocal and engine
- [ ] Implement get_db dependency
- [ ] Implement all CRUD operations
- [ ] Test creating todos (persists to DB)
- [ ] Verify data persists after restart
- [ ] Add stats endpoint
- [ ] Commit to GitHub

---

## 🎯 Day 6: Async, Logging & Settings (2.5 hours)

### What You'll Learn
- Async/await patterns
- Logging configuration
- Environment variables
- Settings management

### Code Example: Async API + Config

```python
from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings
import logging
import httpx
from typing import Optional

# Configuration
class Settings(BaseSettings):
    app_name: str = "FastAPI Crash Course"
    debug: bool = True
    database_url: str = "sqlite:///./todos.db"
    log_level: str = "INFO"
    external_api_url: str = "https://api.github.com"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, debug=settings.debug)

# Dependency: HTTP client
async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client

# GET with async external API call
@app.get("/github/{username}")
async def get_github_user(
    username: str,
    client: httpx.AsyncClient = Depends(get_http_client)
):
    """Fetch GitHub user data asynchronously"""
    logger.info(f"Fetching GitHub user: {username}")
    
    try:
        response = await client.get(
            f"{settings.external_api_url}/users/{username}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Successfully fetched {username}")
            return {
                "username": data.get("login"),
                "name": data.get("name"),
                "bio": data.get("bio"),
                "followers": data.get("followers"),
                "repos": data.get("public_repos")
            }
        else:
            logger.warning(f"GitHub user {username} not found")
            return {"error": "User not found"}
    
    except Exception as e:
        logger.error(f"Error fetching GitHub user: {str(e)}")
        return {"error": "Failed to fetch user"}

# POST with logging
@app.post("/tasks")
async def create_task(task: dict):
    """Create a task with logging"""
    logger.info(f"Creating task: {task}")
    
    # Simulate async work
    import asyncio
    await asyncio.sleep(1)
    
    logger.info(f"Task created successfully")
    return {"id": 1, "status": "created", "task": task}

# GET app configuration
@app.get("/config")
async def get_config():
    """Get current app configuration"""
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "log_level": settings.log_level
    }

# Health check
@app.get("/health")
async def health():
    logger.debug("Health check called")
    return {"status": "healthy"}
```

### .env File

```
APP_NAME=FastAPI Crash Course
DEBUG=true
DATABASE_URL=sqlite:///./todos.db
LOG_LEVEL=INFO
EXTERNAL_API_URL=https://api.github.com
```

### Day 6 Checklist
- [ ] Install: `pip install pydantic-settings httpx`
- [ ] Create Settings class with BaseSettings
- [ ] Create .env file with example values
- [ ] Set up logging configuration
- [ ] Implement async HTTP client dependency
- [ ] Add async endpoint calling external API
- [ ] Test with real GitHub API
- [ ] Verify logging output
- [ ] Commit to GitHub

---

## 🎯 Day 7: Testing & Capstone Project (3 hours)

### What You'll Learn
- pytest basics
- Testing FastAPI apps
- Mocking dependencies
- Coverage reports
- Integration tests

### Code Example: Test Suite

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, Base, get_db, TodoModel

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixtures
@pytest.fixture(autouse=True)
def setup_teardown():
    """Clear database before each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

# Tests
class TestTodos:
    
    def test_create_todo(self):
        """Test creating a todo"""
        response = client.post(
            "/todos",
            json={
                "title": "Test Todo",
                "description": "Test Description",
                "priority": 1
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Todo"
        assert data["completed"] == False
    
    def test_get_todos(self):
        """Test listing todos"""
        # Create test todo
        client.post("/todos", json={"title": "Todo 1"})
        client.post("/todos", json={"title": "Todo 2"})
        
        response = client.get("/todos")
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) == 2
    
    def test_get_single_todo(self):
        """Test getting a single todo"""
        # Create todo
        create_response = client.post("/todos", json={"title": "Test Todo"})
        todo_id = create_response.json()["id"]
        
        # Get it
        response = client.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Test Todo"
    
    def test_update_todo(self):
        """Test updating a todo"""
        # Create todo
        create_response = client.post("/todos", json={"title": "Original"})
        todo_id = create_response.json()["id"]
        
        # Update it
        response = client.put(
            f"/todos/{todo_id}",
            json={"title": "Updated", "description": "New desc"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated"
    
    def test_delete_todo(self):
        """Test deleting a todo"""
        # Create todo
        create_response = client.post("/todos", json={"title": "To Delete"})
        todo_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/todos/{todo_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404
    
    def test_complete_todo(self):
        """Test marking a todo as complete"""
        # Create todo
        create_response = client.post("/todos", json={"title": "Task"})
        todo_id = create_response.json()["id"]
        
        # Complete it
        response = client.patch(f"/todos/{todo_id}/complete")
        assert response.status_code == 200
        assert response.json()["completed"] == True
    
    def test_filter_by_completed(self):
        """Test filtering todos by completion status"""
        # Create todos
        client.post("/todos", json={"title": "Todo 1"})
        create_resp = client.post("/todos", json={"title": "Todo 2"})
        todo_id = create_resp.json()["id"]
        
        # Complete one
        client.patch(f"/todos/{todo_id}/complete")
        
        # Get pending only
        response = client.get("/todos?completed=false")
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) == 1
    
    def test_todo_not_found(self):
        """Test getting non-existent todo"""
        response = client.get("/todos/9999")
        assert response.status_code == 404
    
    def test_get_stats(self):
        """Test stats endpoint"""
        # Create todos
        client.post("/todos", json={"title": "Todo 1"})
        create_resp = client.post("/todos", json={"title": "Todo 2"})
        todo_id = create_resp.json()["id"]
        
        # Complete one
        client.patch(f"/todos/{todo_id}/complete")
        
        response = client.get("/stats")
        assert response.status_code == 200
        stats = response.json()
        assert stats["total"] == 2
        assert stats["completed"] == 1
        assert stats["pending"] == 1
```

### Run Tests

```bash
# Install pytest
pip install pytest

# Run all tests
pytest -v

# Run with coverage
pip install pytest-cov
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_main.py::TestTodos::test_create_todo -v
```

### Capstone Mini-Project: Multi-Feature Todo API

**Build a production-ready Todo API combining all 7 days**:

Requirements:
- ✅ Setup with uvicorn
- ✅ All HTTP methods (GET, POST, PUT, DELETE, PATCH)
- ✅ Query parameters (skip, limit, filters)
- ✅ Pydantic validation
- ✅ Dependencies (logging)
- ✅ SQLAlchemy database persistence
- ✅ Async operations
- ✅ Configuration via .env
- ✅ Comprehensive test suite (>80% coverage)
- ✅ Proper error handling

**Features to Add**:
1. User authentication (Day 4)
2. Todo categories/tags
3. Todo sharing between users
4. Due dates and reminders
5. Priority levels
6. Search functionality
7. Statistics dashboard
8. Export todos to CSV

**Directory Structure**:
```
fastapi-week/
├── main.py              # Main app
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic models
├── database.py          # DB configuration
├── dependencies.py      # Shared dependencies
├── .env                 # Configuration
├── .env.example         # Example config
├── requirements.txt     # Dependencies
├── tests/
│   ├── test_todos.py
│   ├── test_auth.py
│   └── test_integration.py
└── README.md            # Project docs
```

### Day 7 Checklist
- [ ] Install pytest and pytest-cov
- [ ] Write unit tests for all endpoints
- [ ] Write integration tests
- [ ] Achieve >80% code coverage
- [ ] Test edge cases and errors
- [ ] Mock external dependencies
- [ ] Generate coverage report
- [ ] Build capstone project with all features
- [ ] Commit to GitHub with passing tests

---

## 📝 Quick Reference: HTTP Methods

| Method | Purpose | Status | Use Case |
|--------|---------|--------|----------|
| **GET** | Retrieve data | 200 | Fetch todos, search, filter |
| **POST** | Create new data | 201 | Create todo, signup |
| **PUT** | Replace resource | 200 | Update entire todo |
| **DELETE** | Remove data | 204 | Delete todo |
| **PATCH** | Partial update | 200 | Mark todo complete |

---

## 📚 Key Concepts Recap

### Status Codes
- **200** — Success
- **201** — Created
- **204** — No Content (for DELETE)
- **400** — Bad Request (validation error)
- **401** — Unauthorized
- **404** — Not Found
- **409** — Conflict (duplicate)
- **500** — Server Error

### Common Patterns
- Always use proper status codes
- Return meaningful error messages
- Validate input early
- Use async for I/O operations
- Log important operations
- Write tests for all endpoints
- Use environment variables for config
- Implement proper error handling

---

## 📦 Final Requirements.txt

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
pydantic[email]==2.5.0
pyjwt==2.8.1
python-multipart==0.0.6
httpx==0.25.2
pytest==7.4.3
pytest-cov==4.1.0
```


## 💡 Pro Tips

1. **Always test your code** — Write tests as you build
2. **Use type hints** — FastAPI magic relies on them
3. **Read error messages** — Pydantic provides helpful feedback
4. **Start simple** — Build incrementally
5. **Commit frequently** — Push to GitHub daily
6. **Read docs** — FastAPI docs are excellent
7. **Use Swagger UI** — Test endpoints before writing frontend
8. **Environment variables** — Never hardcode secrets

---

## 🚀 Deployment Quick Links

After 1 week, you're ready to:
- Deploy to Heroku
- Deploy to Railway
- Deploy to Render
- Deploy to AWS EC2
- Containerize with Docker

---

**Congratulations on completing FastAPI Crash Course! 🎉**

You now understand:
- HTTP methods and REST principles
- Request/response handling
- Data validation with Pydantic
- Authentication and authorization
- Database integration
- Async programming basics
- Testing and configuration management

**Next Step**: Pick a real project and build it!
