# CQRS with Python, FastAPI, PostgreSQL & MongoDB

A clean, minimal implementation of the **CQRS (Command Query Responsibility Segregation)** pattern using FastAPI, PostgreSQL for writes, and MongoDB for reads.

Built as the companion project for the Medium article: [Building a Scalable CQRS Architecture in Python](#).

> By [Adxell Arango](https://www.linkedin.com/in/adxell-adrian-arango-solano-9b302a149/)

---

## Architecture Overview

```
Client
  │
  ├──► POST /commands/orders  →  Command Handler  →  PostgreSQL (source of truth)
  │                                                         │
  │                                                   Domain Event
  │                                                         │
  │                                                    Event Bus
  │                                                         │
  │                                                    Projector  →  MongoDB (read model)
  │
  └──► GET /queries/orders/{id}  →  Query Handler  →  MongoDB
```

**Write side (PostgreSQL):** Enforces business rules, ACID transactions, strong consistency.

**Read side (MongoDB):** Pre-computed documents, sub-millisecond reads, no joins needed.

---

## Project Structure

```
cqrs_project/
├── main.py
├── config/
│   └── settings.py
├── domain/
│   ├── models.py        # SQLAlchemy models (PostgreSQL)
│   └── events.py        # Immutable domain events
├── commands/
│   ├── schemas.py       # Pydantic input validation
│   └── handlers.py      # Business logic + DB writes
├── queries/
│   ├── schemas.py       # Response schemas
│   └── handlers.py      # Reads from MongoDB
├── infrastructure/
│   ├── pg_database.py   # PostgreSQL async session
│   ├── mongo_database.py
│   └── event_bus.py     # In-memory async event bus
└── projectors/
    └── handlers.py      # Syncs events → MongoDB
```

---

## Getting Started

### 1. Clone and configure

```bash
git clone https://github.com/your-username/cqrs-python-fastapi.git
cd cqrs-python-fastapi
cp .env.example .env
```

### 2. Run with Docker

```bash
docker-compose up --build
```

### 3. Or run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start PostgreSQL and MongoDB locally, then:
cd cqrs_project
uvicorn main:app --reload
```

API docs available at: **http://localhost:8000/docs**

---

## Key Concepts

| Concept | Where |
|---|---|
| Command validation | `commands/schemas.py` |
| Business logic + PostgreSQL write | `commands/handlers.py` |
| Domain event emission | `domain/events.py` |
| Async event routing | `infrastructure/event_bus.py` |
| MongoDB sync | `projectors/handlers.py` |
| Fast reads from MongoDB | `queries/handlers.py` |

---

## Stack

- **FastAPI** — async web framework
- **SQLAlchemy (async)** — ORM for PostgreSQL
- **Motor** — async MongoDB driver
- **Pydantic v2** — data validation
- **Docker Compose** — local dev environment

---

## Author

**Adxell Arango** — Systems Engineer & Full-Stack Developer  
[LinkedIn](https://www.linkedin.com/in/adxell-adrian-arango-solano-9b302a149/) | [Snaaply](https://snaaply.com)
