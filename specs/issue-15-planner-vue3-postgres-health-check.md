# Plan: Create Vue 3 Index Page with PostgreSQL Health Check via FastAPI

## Description
Create a simple Vue 3 index page that displays whether a PostgreSQL database connection is successful or not. The page will communicate with a FastAPI backend that checks the PostgreSQL connection status and returns the result.

This is a greenfield project - the `app/` directory needs to be created from scratch with:
1. A FastAPI backend (`app/server/`) that connects to PostgreSQL and exposes a `/health` endpoint
2. A Vue 3 frontend (`app/client/`) that calls the health endpoint and displays connection status

## Relevant Files
Use these files to resolve the chore:

- `scripts/` - Contains utility scripts; will need new scripts for starting server and client

### New Files

**Backend (app/server/):**
- `app/server/pyproject.toml` - Python dependencies for FastAPI and PostgreSQL
- `app/server/main.py` - FastAPI application with health check endpoint
- `app/server/database.py` - PostgreSQL connection and health check logic
- `app/server/.env.sample` - Database connection environment variables template
- `app/server/tests/test_health.py` - Tests for the health endpoint
- `app/server/tests/__init__.py` - Test package init

**Frontend (app/client/):**
- `app/client/package.json` - Node.js dependencies for Vue 3 and Vite
- `app/client/vite.config.js` - Vite configuration with API proxy
- `app/client/index.html` - HTML entry point
- `app/client/src/main.js` - Vue 3 application entry
- `app/client/src/App.vue` - Main component with health check display
- `app/client/src/style.css` - Basic styling

**Project Root:**
- `README.md` - Project documentation with setup and run instructions

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Directory Structure
- Create `app/server/` directory
- Create `app/server/tests/` directory
- Create `app/client/` directory
- Create `app/client/src/` directory

### Step 2: Create FastAPI Backend - Dependencies
- Create `app/server/pyproject.toml`:
```toml
[project]
name = "valargen-server"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "asyncpg>=0.29.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.26.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Step 3: Create FastAPI Backend - Environment Template
- Create `app/server/.env.sample`:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/valargen
```

### Step 4: Create FastAPI Backend - Database Module
- Create `app/server/database.py`:
  - Import asyncpg and os
  - Create async function `check_database_connection()` that:
    - Reads DATABASE_URL from environment
    - Attempts to connect to PostgreSQL using asyncpg
    - Returns `{"status": "connected", "database": "postgresql"}` on success
    - Returns `{"status": "disconnected", "error": "<message>"}` on failure
    - Properly closes connection in finally block

### Step 5: Create FastAPI Backend - Main Application
- Create `app/server/main.py`:
  - Import FastAPI, CORSMiddleware
  - Import check_database_connection from database module
  - Load environment variables using python-dotenv
  - Create FastAPI app instance
  - Add CORS middleware allowing all origins (for development)
  - Create `GET /health` endpoint that calls check_database_connection()
  - Create `GET /` root endpoint returning `{"message": "Valargen API"}`

### Step 6: Create FastAPI Backend - Tests
- Create `app/server/tests/__init__.py` (empty file)
- Create `app/server/tests/test_health.py`:
  - Import TestClient from fastapi.testclient
  - Import app from main
  - Test that GET /health returns 200 status
  - Test that response has "status" field
  - Test that GET / returns 200 with message

### Step 7: Create Vue 3 Frontend - Package Configuration
- Create `app/client/package.json`:
```json
{
  "name": "valargen-client",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0"
  }
}
```

### Step 8: Create Vue 3 Frontend - Vite Configuration
- Create `app/client/vite.config.js`:
  - Import defineConfig from vite
  - Import vue plugin from @vitejs/plugin-vue
  - Configure proxy to forward `/api` requests to `http://localhost:8000`
  - Export config with vue plugin

### Step 9: Create Vue 3 Frontend - HTML Entry
- Create `app/client/index.html`:
  - Standard HTML5 doctype
  - Title: "Valargen - PostgreSQL Health Check"
  - Root div with id="app"
  - Script module src pointing to /src/main.js

### Step 10: Create Vue 3 Frontend - Vue Application Entry
- Create `app/client/src/main.js`:
  - Import createApp from vue
  - Import App component
  - Import style.css
  - Mount app to #app element

### Step 11: Create Vue 3 Frontend - Main Component
- Create `app/client/src/App.vue`:
  - Template section:
    - Container div with class "app"
    - H1 title: "PostgreSQL Connection Status"
    - Loading state: "Checking connection..."
    - Connected state (green): "Connected to PostgreSQL"
    - Disconnected state (red): "Disconnected" with error message
    - Button to retry connection check
  - Script setup section:
    - Import ref and onMounted from vue
    - Create reactive refs: status, loading, error
    - Create checkHealth async function that fetches /api/health
    - Call checkHealth in onMounted
  - Style section (scoped):
    - Center content
    - Green color for connected status
    - Red color for disconnected status
    - Basic button styling

### Step 12: Create Vue 3 Frontend - Styles
- Create `app/client/src/style.css`:
  - CSS reset (box-sizing, margin, padding)
  - Body styling with light background
  - Container centering
  - Status indicator colors

### Step 13: Create Project README
- Create `README.md` at project root with:
  - Project title and description
  - Prerequisites (Python 3.11+, Node.js 18+, PostgreSQL, uv)
  - Backend setup instructions (cd app/server, uv sync, copy .env)
  - Frontend setup instructions (cd app/client, npm install)
  - How to run backend: `cd app/server && uv run uvicorn main:app --reload`
  - How to run frontend: `cd app/client && npm run dev`
  - Default URLs: Backend http://localhost:8000, Frontend http://localhost:5173

### Step 14: Run Validation Commands
- Execute all validation commands to verify the implementation

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv sync` - Install server dependencies
- `cd app/server && uv run pytest` - Run server tests
- `cd app/client && npm install` - Install client dependencies
- `cd app/client && npm run build` - Build client to verify no errors

## Notes
- PostgreSQL must be running for full integration testing
- The frontend uses Vite's proxy to avoid CORS issues during development
- Default database URL assumes PostgreSQL running locally with default credentials
- The health check is designed to gracefully handle connection failures
- Environment variables must be configured before running the server
