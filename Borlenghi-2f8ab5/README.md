# Notes App — Full Stack Technical Challenge

A SPA notes application with tagging, filtering, and archiving capabilities.  
Backend: **FastAPI** (Python) with layered architecture  
Frontend: **React** with Zustand state management  

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Setup & Run](#setup--run)
  - [Option 1: One-command setup (recommended)](#option-1-one-command-setup-recommended)
  - [Option 2: Manual setup](#option-2-manual-setup)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [License](#license)

---

## 🎯 Overview

This application allows users to:
- Create, edit, delete notes
- Archive/unarchive notes
- List active/archived notes
- Assign categories to notes (Phase 2)
- Filter notes by category and archive status

Built as a solution to the Full Stack Technical Challenge.

## ✨ Features

**Phase 1 (Mandatory):**
- ✅ Create, edit, delete notes
- ✅ Archive/unarchive notes
- ✅ List active notes
- ✅ List archived notes

**Phase 2 (Extra points):**
- ✅ Add/remove categories to notes
- ✅ Filter notes by category

**Additional:**
- ✅ JWT-based authentication (stateless)
- ✅ Layered backend architecture (Controllers → Services → DAOs)
- ✅ SQLite persistence via SQLModel ORM
- ✅ React SPA with React Router v6
- ✅ Zustand for global state (auth, notes, categories, filters)
- ✅ React Hook Form for form validation
- ✅ CSS Modules for scoped styling
- ✅ One-command setup script (`setup.sh`)
- ✅ Full CRUD with proper HTTP status codes
- ✅ Protected routes (authentication required)

## 🛠️ Tech Stack

### Backend
| Component          | Version         | Purpose                                  |
|--------------------|-----------------|------------------------------------------|
| Python             | 3.12.3          | Runtime                                  |
| FastAPI            | 0.115.6         | Web framework                            |
| Uvicorn            | 0.34.0          | ASGI server                              |
| SQLModel           | 0.0.22          | ORM + validation                         |
| Pydantic           | 2.10.4          | Data validation                          |
| PyJWT              | 2.10.1          | JSON Web Tokens                          |
| python-dotenv      | 1.0.1           | Environment variables                    |
| HTTPX              | 0.28.1          | HTTP client (for tests)                  |
| Pytest             | 8.3.4           | Testing framework                        |
| Pytest-asyncio     | 0.25.0          | Async test support                       |

### Frontend
| Component               | Version        | Purpose                                  |
|-------------------------|----------------|------------------------------------------|
| React                   | 18.3.1         | UI library                               |
| React DOM               | 18.3.1         | DOM bindings                             |
| React Router DOM        | 6.28.1         | Client-side routing                      |
| React Hook Form         | 7.54.2         | Form validation                          |
| Zustand                 | 5.0.3          | State management                         |
| Axios                   | 1.7.9          | HTTP client                              |
| Vite                    | 6.4.1          | Build tool & dev server                  |
| @vitejs/plugin-react    | 4.3.4          | React plugin for Vite                    |

### DevTools
- **Git** – Version control
- **bash** – Setup script (`setup.sh`)

## 🏗️ Architecture

### Backend (3-layer)
```
Controllers (API routers)
    ↓
Services (business logic)
    ↓
DAOs (data access)
    ↓
SQLModel (SQLite)
```

**Key Decisions:**
- **Controllers**: Handle HTTP requests/responses, validation, authentication
- **Services**: Contain business rules (archive validation, category existence checks)
- **DAOs**: Abstract persistence layer (SQLModel CRUD operations)
- **Models**: SQLModel classes with relationships (Note ↔ Category)
- **Schemas**: Pydantic models for request/response validation
- **Auth**: JWT stateless authentication (hardcoded demo user: `admin/admin`)
- **CORS**: Configured to allow frontend dev origins

### Frontend
```
index.html
    ↓
main.jsx (React root + BrowserRouter)
    ↓
App.jsx (routes)
    ↓
├── /login → Login.jsx
    ↓
├── /notes → NotesPage.jsx (protected)
    ↓
├── Components: NoteCard, NoteForm
    ↓
├── Store: Zustand (auth token, notes, categories, filters)
    ↓
├── Services: API wrappers (Axios + auth interceptor)
    ↓
└── Styles: CSS Modules + CSS variables
```

**State Management:**
- Zustand store holds:
  - `token`: JWT string (synced with localStorage)
  - `notes`: Array of note objects
  - `categories`: Array of category objects
  - `filterArchived`: null/all/archived/active
  - `filterCategory`: null/categoryId
- Actions to update state and persist via API

**Data Flow Example (Create Note):**
1. User submits form in `NoteForm` (React Hook Form)
2. `NotesPage.handleCreate()` calls `noteService.createNote()`
3. `noteService` → Axios → `/api/notes` (POST) with JWT header
4. Backend: Auth middleware → Notes endpoint → Service → DAO → SQLModel insert
5. On success: Store updated via `addNote()` action, form resets

## 🚀 Setup & Run

### Option 1: One-command setup (recommended)

```bash
# Clone repo (if not already)
git clone <repository-url>
cd Borlenghi-2f8ab5

# Make executable and run
chmod +x setup.sh
./setup.sh
```

The script will:
1. Check prerequisites (Python, Node.js runtime, npm/bun)
2. Create backend virtual environment (uses `uv` if available, else `python3 -m venv`)
3. Install backend dependencies (`requirements.txt`)
4. Seed SQLite database with 5 categories and 3 sample notes
5. Install frontend dependencies (`package.json`)
6. Start both servers:
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:5173` (via Vite dev server)
   - API docs: `http://localhost:8000/docs`

**To stop:** Press `Ctrl+C` in the terminal.

### Option 2: Manual setup

#### Backend
```bash
cd backend

# Python 3.8+ required
python3 -m venv venv          # or: uv venv venv
source venv/bin/activate      # or: .\venv\Scripts\activate on Windows
pip install -r requirements.txt  # or: uv pip install -r requirements.txt

# Seed database
rm -f data/notes.db           # start fresh
python seed_data.py

# Run server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend

# Node.js required (v18+ recommended)
npm install                   # or: bun install

# Run dev server
npm run dev                   # or: bun dev
# Vite will start on http://localhost:5173
# Proxy configured to forward /api requests to http://localhost:8000
```

#### First Login
- Username: `admin`
- Password: `admin`

## 🔌 API Endpoints

All endpoints require JWT token in `Authorization: Bearer <token>` header (except login).

| Method | Endpoint                  | Description                     | Auth | Status Codes          |
|--------|---------------------------|---------------------------------|------|-----------------------|
| `POST` | `/api/auth/login`         | Login (demo: admin/admin)       | ❌   | 200 (token), 401      |
| `GET`  | `/api/notes`              | List notes (filter: archived?, category_id?) | ✅   | 200 ([] or [Note])   |
| `POST` | `/api/notes`              | Create note                     | ✅   | 201 (Note), 422       |
| `GET`  | `/api/notes/{id}`         | Get note by ID                  | ✅   | 200 (Note), 404       |
| `PUT`  | `/api/notes/{id}`         | Update note (title/content)     | ✅   | 200 (Note), 404, 422  |
| `DELETE`| `/api/notes/{id}`        | Delete note                     | ✅   | 204, 404              |
| `PATCH`| `/api/notes/{id}/archive` | Toggle archive flag             | ✅   | 200 (Note), 404       |
| `PATCH`| `/api/notes/{id}/category`| Assign/remove category          | ✅   | 200 (Note), 404, 422  |
| `GET`  | `/api/categories`         | List all categories             | ✅   | 200 ([Category])      |
| `GET`  | `/api/health`             | Health check                    | ❌   | 200 ({status: "ok"})  |

### Models (JSON)

**Note:**
```json
{
  "id": 1,
  "title": "string",
  "content": "string",
  "is_archived": boolean,
  "category_id": integer | null
}
```

**Category:**
```json
{
  "id": 1,
  "name": "string"
}
```

**Auth:**
```json
// Login request
{
  "username": "string",
  "password": "string"
}

// Login response
{
  "access_token": "jwt-token-string",
  "token_type": "bearer"
}
```

## 🧪 Testing

### Backend
Run unit and integration tests:
```bash
cd backend
source venv/bin/activate
pytest -v
```

### Frontend
Frontend unit tests are not included in this challenge (per spec), but the structure supports adding Jest + React Testing Library later.

## 📁 Project Structure

```
Borlenghi-2f8ab5/
├── backend/                  # Backend source code
│   ├── app/                  # Python package
│   │   ├── api/              # API routers & endpoints
│   │   ├── core/             # Config, security, auth, database
│   │   ├── dao/              # Data access layer
│   │   ├── models/           # SQLModel models (Note, Category)
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic layer
│   ├── data/                 # SQLite database (auto-created)
│   ├── seed_data.py          # Seed categories + sample notes
│   ├── requirements.txt      # Python dependencies
│   ├── run.py                # Uvicorn entry point
│   └── setup_backend.sh      # (internal) backend-only setup
├── frontend/                 # Frontend source code
│   ├── public/               # Static assets
│   │   └── index.html        # SPA entry point
│   ├── src/                  # React source
│   │   ├── components/       # Reusable UI (NoteCard, NoteForm)
│   │   ├── pages/            # Page components (Login, NotesPage)
│   │   ├── routes/           # Route guards (ProtectedRoute)
│   │   ├── services/         # API wrappers (Axios interceptors)
│   │   ├── store/            # Zustand store
│   │   ├── styles/           # CSS (globals + modules)
│   │   ├── App.jsx           # Main app with routes
│   │   └── main.jsx          # React root
│   ├── index.html            # SPA shell
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js        # Vite config (with /api proxy)
├/setup.sh                  # One-command setup & run script
├── README.md                 # This file
└── design.md                 # Technical design document
```

## 📝 Notes

- **Database**: SQLite file `backend/data/notes.db` is auto-created on first run.  
  To reset: delete the file and re-run `seed_data.py` or `./setup.sh`.
- **Auth**: For demo purposes, uses hardcoded credentials (`admin/admin`).  
  In production, replace with proper user store and password hashing.
- **CORS**: Configured to allow `http://localhost:5173` and `http://localhost:3000`.  
  Adjust `backend/app/main.py` if frontend runs on different port.
- **State**: Zustand store keeps auth token in memory only; token is also saved to `localStorage`  
  and cleared on logout/page reload (intentional for challenge simplicity).
- **CSS**: Uses CSS Variables for theming and CSS Modules for component-scoped styles.

## 📄 License

This project is created for the Full Stack Technical Challenge.  
Please refer to the repository license for usage rights.

---

**Happy coding!** 🚀  
*Built with ❤️ using FastAPI, React, and Zustand.*