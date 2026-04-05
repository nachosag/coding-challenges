# Design: Notes Application — Prueba Técnica Full Stack

## Technical Approach

We will implement a layered backend (FastAPI) and a React SPA frontend, following the spec and user decisions. The backend uses three layers: controllers (routers), services (business logic), and DAOs (data access via SQLModel). The frontend uses React Router v6 for navigation, React Hook Form for form handling, and Zustand for global state management (notes, categories, auth). CSS will be vanilla/CSS modules. Setup script automates venv creation, dependency installation, DB seeding, and concurrent server startup.

## Architecture Decisions

### Decision: Backend Layered Architecture

**Choice**: 3-layer architecture: Controllers → Services → DAOs  
**Alternatives considered**: MVC, single-layer (direct SQLModel in routers), Clean Architecture with use cases  
**Rationale**: Matches spec NFR-03, provides clear separation, testability, and scalability for this challenge. Controllers handle HTTP, services encapsulate business rules (archive, category assignment), DAOs abstract persistence.

### Decision: State Management with Zustand

**Choice**: Zustand for global state (auth token, notes list, categories, UI filters)  
**Alternatives considered**: React Context API + useReducer, Redux Toolkit, Zustand  
**Rationale**: User explicitly requested Zustand; it offers minimal boilerplate, fine-grained subscriptions, and middleware support. Local form state remains with React Hook Form.

### Decision: SQLite with SQLModel

**Choice**: SQLite file database, SQLModel ORM  
**Alternatives considered**: PostgreSQL, raw sqlite3, Tortoise ORM  
**Rationale**: Spec NFR-02 mandates SQLite auto-created by SQLModel; suitable for challenge scope, zero config, and SQLModel provides Pythonic models with validation.

### Decision: Authentication via JWT (stateless)

**Choice**: JWT token returned on login, stored in frontend state, sent via Authorization header  
**Alternatives considered**: HTTP Basic, server-side sessions  
**Rationale**: Stateless, simple to implement, works with SPA; spec REQ-01 expects a token. We'll use PyJWT with a hardcoded secret for demo.

### Decision: CSS Approach

**Choice**: CSS Modules for component-scoped styles, CSS variables for theme  
**Alternatives considered**: Vanilla CSS, Tailwind (excluded by user), CSS-in-JS  
**Rationale**: User said no Tailwind; CSS Modules provide encapsulation without runtime overhead.

## Data Flow

### Login Flow
```
Frontend Login Form ──(POST /api/auth/login)──→ Backend Controller
                                               ↓
                                           Service (validate creds)
                                               ↓
                                           DAO (none — check hardcoded)
                                               ↓
                                   Controller ←─(200 + {token})─ Backend
                                               ↓
                                   Frontend stores token in Zustand
                                               ↓
                                   Redirect to /notes
```

### Create Note Flow
```
Frontend Form ──(POST /api/notes, JSON, Auth header)──→ Controller
                                               ↓
                                   Service (validate title/content)
                                               ↓
                                           DAO (SQLModel insert)
                                               ↓
                                   Controller ←─(201 + Note)─ Backend
                                               ↓
                                   Frontend updates notes list via Zustand
```

### Archive Note Flow
```
Frontend Button ──(PATCH /api/notes/{id}/archive, {is_archived})──→ Controller
                                               ↓
                                   Service (toggle archived flag)
                                               ↓
                                           DAO (SQLModel update)
                                               ↓
                                   Controller ←─(200 + UpdatedNote)─ Backend
                                               ↓
                                   Frontend updates note in Zustand list
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/app/main.py` | Create | FastAPI app creation, router inclusion, middleware (CORS, auth) |
| `backend/app/core/config.py` | Create | Settings (JWT secret, token expiry) |
| `backend/app/core/security.py` | Create | JWT create/verify utilities |
| `backend/app/core/auth.py` | Create | Dependency for protecting routes |
| `backend/app/api/deps.py` | Create | Dependency injection (DB session) |
| `backend/app/api/v1/router.py` | Create | Versioned API router aggregating sub-routers |
| `backend/app/api/v1/endpoints/auth.py` | Create | Login endpoint |
| `backend/app/api/v1/endpoints/notes.py` | Create | CRUD, archive, category endpoints for notes |
| `backend/app/api/v1/endpoints/categories.py` | Create | List categories endpoint (Phase 2) |
| `backend/app/services/note_service.py` | Create | Business logic: create, update, delete, archive, assign category |
| `backend/app/services/category_service.py` | Create | Fetch categories (Phase 2) |
| `backend/app/dao/note_dao.py` | Create | SQLModel CRUD operations for Note |
| `backend/app/dao/category_dao.py` | Create | SQLModel CRUD for Category (Phase 2) |
| `backend/app/models/note.py` | Create | SQLModel Note model (id, title, content, is_archived, category_id) |
| `backend/app/models/category.py` | Create | SQLModel Category model (id, name) |
| `backend/app/schemas/note.py` | Create | Pydantic schemas (NoteCreate, NoteUpdate, NoteInDB) |
| `backend/app/schemas/category.py` | Create | Pydantic schemas for Category |
| `backend/data/notes.db` | Create | SQLite file (auto-generated on first run) |
| `backend/seed_data.py` | Create | Seed categories and test notes |
| `backend/requirements.txt` | Create | Backend dependencies (fastapi, sqlmodel, uvicorn, pydantic, pyjwt, pytest, httpx) |
| `backend/.env` | Create | Environment variables (SECRET_KEY) |
| `frontend/package.json` | Create | Frontend deps (react, react-dom, react-router-dom, zustand, react-hook-form) |
| `frontend/src/index.jsx` | Create | React root, Provider from Zustand |
| `frontend/src/App.jsx` | Create | Main app with routes |
| `frontend/src/routes/ProtectedRoute.jsx` | Create | Wrapper requiring auth |
| `frontend/src/pages/Login.jsx` | Create | Login form (React Hook Form) |
| `frontend/src/pages/NotesPage.jsx` | Create | Lists active/archived notes, filter controls |
| `frontend/src/components/NoteCard.jsx` | Create | Displays note, edit/archive/category buttons |
| `frontend/src/components/NoteForm.jsx` | Create | Create/edit form (React Hook Form) |
| `frontend/src/store/useStore.jsx` | Create | Zustand store (auth token, notes, categories, filters) |
| `frontend/src/services/api.js` | Create | Axios instance with auth interceptor |
| `frontend/src/services/noteService.js` | Create | Wrapper for notes API endpoints |
| `frontend/src/services/categoryService.js` | Create | Wrapper for categories API (Phase 2) |
| `frontend/src/styles/globals.css` | Create | CSS variables, base styles |
| `frontend/src/styles/NoteCard.module.css` | Create | Component-scoped styling |
| `setup.sh` | Create | Bootstraps venv, installs deps, seeds DB, starts servers |
| `README.md` | Create | Project overview, tech stack, setup instructions, API docs |

## Interfaces / Contracts

### OpenAPI Snippet (YAML)
```yaml
openapi: 3.0.3
info:
  title: Notes API
  version: 1.0.0
paths:
  /api/auth/login:
    post:
      summary: Login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
      responses:
        '200':
          description: Token
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Token'
        '401':
          description: Invalid credentials
  /api/notes:
    get:
      summary: List notes
      parameters:
        - name: archived
          in: query
          schema:
            type: boolean
        - name: category_id
          in: query
          schema:
            type: integer
          nullable: true
      responses:
        '200':
          description: Paginated list of notes
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Note'
    post:
      summary: Create note
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NoteCreate'
      responses:
        '201':
          description: Created note
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Note'
  /api/notes/{id}:
    get:
      summary: Get note by id
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Note
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Note'
        '404':
          description: Not found
    put:
      summary: Update note
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NoteUpdate'
      responses:
        '200':
          description: Updated note
        '404':
          description: Not found
    delete:
      summary: Delete note
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '204':
          description: Deleted
        '404':
          description: Not found
    patch:
      summary: Archive toggle
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ArchiveRequest'
      responses:
        '200':
          description: Updated note
        '404':
          description: Not found
    /api/notes/{id}/category:
      patch:
        summary: Assign/remove category
        parameters:
          - name: id
            in: path
            required: true
            schema:
              type: integer
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CategoryRequest'
        responses:
          '200':
            description: Updated note
          '404':
            description: Not found
          '422':
            description: Invalid category_id
  /api/categories:
    get:
      summary: List categories (Phase 2)
      responses:
        '200':
          description: Category list
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Category'
components:
  schemas:
    LoginRequest:
      type: object
      properties:
        username:
          type: string
        password:
          type: string
    Token:
      type: object
      properties:
        access_token:
          type: string
        token_type:
          type: string
          default: bearer
    Note:
      type: object
      properties:
        id:
          type: integer
        title:
          type: string
        content:
          type: string
        is_archived:
          type: boolean
        category_id:
          type: integer
          nullable: true
    NoteCreate:
      required: [title, content]
      type: object
      properties:
        title:
          type: string
          minLength: 1
        content:
          type: string
        category_id:
          type: integer
          nullable: true
    NoteUpdate:
      required: [title, content]
      type: object
      properties:
        title:
          type: string
          minLength: 1
        content:
          type: string
    ArchiveRequest:
      type: object
      required: [is_archived]
      properties:
        is_archived:
          type: boolean
    CategoryRequest:
      type: object
      properties:
        category_id:
          type: integer
          nullable: true
    Category:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit (Backend) | Services (note_service, category_service) – business logic, validation | pytest with mocking of DAOs; test edge cases (empty title, invalid category) |
| Unit (Backend) | DAOs – CRUD operations | pytest using an in-memory SQLite fixture; verify SQLModel interactions |
| Integration (Backend) | API endpoints – full stack request/response, DB persistence | pytest + httpx AsyncClient against test DB; cover auth, CRUD, archive, category filtering |
| Unit (Frontend) | Hooks (useStore) – state updates | Jest + @testing-library/react-hooks; simulate actions |
| Unit (Frontend) | Components (Login, NoteForm, NoteCard) – UI behavior, form validation | React Testing Library; mock api service |
| Integration (Frontend) | Page flows – login → note creation → archive | React Testing Library + MSW (Mock Service Worker) to intercept API calls |
| E2E | Not prioritized (per spec) | None |

Goal: ≥80% coverage on backend services and DAOs; frontend unit coverage on complex hooks and forms.

## Migration / Rollout

**No migration required.** The application uses a fresh SQLite file on each setup; data is ephemeral for the challenge. To reset, delete `backend/data/notes.db` and re-run setup.sh.

Rollback plan: Git branching strategy – `main` stable, develop `feature/phase-1`. If Phase 2 (categories) introduces bugs, merge only Phase 1 and document pending work.

## Open Questions

- [ ] Should we use HTTP Basic instead of JWT to simplify? (JWT chosen for token-based auth as per spec)
- [ ] Should Zustand persist auth token in localStorage for refresh? Decided: keep in memory only; login required on reload (acceptable for challenge).
- [ ] Should we add loading/error states in frontend? Yes, minimal implementation in API service.

## Next Step
Ready for tasks (sdd-tasks).