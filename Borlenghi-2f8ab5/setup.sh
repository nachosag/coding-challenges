#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# ─── Check prerequisites ──────────────────────────────────────
echo ""
echo "========================================="
echo "  Notes App — Setup & Run"
echo "========================================="
echo ""

command -v python3 >/dev/null 2>&1 || error "python3 is required but not found"
command -v node    >/dev/null 2>&1 || error "node is required but not found"
command -v npm     >/dev/null 2>&1 || error "npm is required but not found"

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
NODE_VERSION=$(node --version)
info "Python $PYTHON_VERSION"
info "Node $NODE_VERSION"

# ─── Backend setup ─────────────────────────────────────────────
echo ""
echo "--- Backend Setup ---"

# Detect package manager
if command -v uv >/dev/null 2>&1; then
    info "Using uv (fast)"
else
    # Check if python3 -m venv works
    python3 -m venv /tmp/_test_venv_check 2>/dev/null && rm -rf /tmp/_test_venv_check || {
        error "Cannot create venv. Install one of:\n  - uv:     curl -LsSf https://astral.sh/uv/install.sh | sh\n  - python3-venv (Debian/Ubuntu): sudo apt install python3-venv"
    }
    info "Using python3 -m venv"
fi

# Create venv
if [ ! -d "$BACKEND_DIR/venv" ]; then
    info "Creating virtual environment..."
    if command -v uv >/dev/null 2>&1; then
        uv venv "$BACKEND_DIR/venv" >/dev/null 2>&1
    else
        python3 -m venv "$BACKEND_DIR/venv" 2>/dev/null || {
            error "Failed to create venv.\n  Try: sudo apt install python3-venv\n  Or: curl -LsSf https://astral.sh/uv/install.sh | sh"
        }
    fi
fi
PYTHON_VENV="$BACKEND_DIR/venv/bin/python"

# Install dependencies
info "Installing backend dependencies..."
if command -v uv >/dev/null 2>&1; then
    uv pip install -r "$BACKEND_DIR/requirements.txt" --python "$PYTHON_VENV" >/dev/null 2>&1
else
    "$BACKEND_DIR/venv/bin/pip" install -r "$BACKEND_DIR/requirements.txt" >/dev/null 2>&1
fi

info "Backend dependencies installed"

# Seed database
cd "$BACKEND_DIR"
rm -f data/notes.db
"$PYTHON_VENV" seed_data.py
info "Database seeded (5 categories, 3 sample notes)"

# ─── Frontend setup ────────────────────────────────────────────
echo ""
echo "--- Frontend Setup ---"

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    info "Installing frontend dependencies..."
    cd "$FRONTEND_DIR"
    $NPM_CMD install >/dev/null 2>&1
else
    info "Frontend dependencies already installed"
fi

# ─── Start servers ─────────────────────────────────────────────
echo ""
echo "--- Starting Servers ---"
echo ""
info "Backend:  http://localhost:8000"
info "Frontend: http://localhost:5173"
info "API Docs: http://localhost:8000/docs"
echo ""
warn "Press Ctrl+C to stop both servers"
echo ""

# Cleanup on exit
cleanup() {
    echo ""
    info "Shutting down..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}
trap cleanup INT TERM

# Start backend
cd "$BACKEND_DIR"
"$PYTHON_VENV" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
cd "$FRONTEND_DIR"
if [ "$NODE_CMD" = "bun" ]; then
    bun vite --host 0.0.0.0 --port 5173 &
else
    npx vite --host 0.0.0.0 --port 5173 &
fi
FRONTEND_PID=$!

echo ""
info "✅ Aplicación lista!"
info "   Frontend: http://localhost:5173"
info "   Backend API: http://localhost:8000"
info "   Docs: http://localhost:8000/docs"
info ""
warn "Presione Ctrl+C para detener ambos servidores"
echo ""

# Wait for both
wait $BACKEND_PID $FRONTEND_PID
