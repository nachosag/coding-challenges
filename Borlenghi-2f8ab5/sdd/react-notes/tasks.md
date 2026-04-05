# Tasks: React Notes Frontend Store & Services

## Phase 1: State Management & API Layer

- [x] Create `frontend/src/store/useStore.js` — Zustand store
- [x] Create `frontend/src/services/api.js` — Axios instance with auth interceptor
- [x] Create `frontend/src/services/noteService.js` — Notes API wrapper

## Phase 2: UI Components

- [x] Create `frontend/src/pages/NotesPage.jsx` — Main notes page with filters, CRUD, archive toggle

## Notes

- Implementation follows design.md decisions (Zustand for state, Axios with interceptors)
- Token consistency: store token used for auth guard; localStorage token used for API interceptor; login page must sync both
- Store logout does not clear localStorage (potential issue for future fix)