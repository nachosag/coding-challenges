# coding-challenges

Repositorio que agrupa mis soluciones a distintos challenges técnicos de coding, abarcando full-stack, backend y blockchain.

## Challenges

### 📝 Borlenghi — Notes App (Full Stack)

Challenge de **Ensolvers** para implementar una SPA de notas con tagging, filtrado y archivado.

| Área | Stack |
|---|---|
| Backend | **FastAPI** (Python 3.12), SQLModel, SQLite, JWT, Pydantic |
| Frontend | **React 18**, Zustand 5, React Router v6, React Hook Form, Vite, CSS Modules |
| Testing | Pytest (async), HTTPX |

- Arquitectura 3-capas: Controllers → Services → DAOs
- Auth JWT stateless (demo: `admin` / `admin`)
- Setup con un solo comando: `./setup.sh`

📍 [`Borlenghi-2f8ab5/`](./Borlenghi-2f8ab5)

---

### ⚙️ CodeSignal — Task Management System

Challenge de **CodeSignal** para implementar un sistema de gestión de tareas con niveles progresivos.

| Concepto | Detalle |
|---|---|
| Lenguaje | Por definir (solo se entrega la descripción del challenge) |
| Nivel 1 | CRUD básico de tareas |
| Nivel 2 | Búsqueda y ordenamiento por prioridad |
| Nivel 3 | Usuarios, TTL, cuotas dinámicas |
| Nivel 4 | Tracking de completitud y análisis histórico |

📍 [`codeSignal-challenge/`](./codeSignal-challenge)

---

### 🔗 Wonderland — Automation Workable Alert (Blockchain)

Challenge de **Wonderland** para desarrollar un monitor on-chain que detecta cuándo un job activo del Sequencer de MakerDAO ha sido trabajado y envía alertas.

| Componente | Stack |
|---|---|
| Runtime | **Node.js** + **TypeScript** (ESM) |
| Blockchain | **ethers v6**, RPC provider |
| Notificadores | Discord (webhook), Console |
| Testing | **Vitest** |
| Build | **tsx** (dev), **tsc** (build) |
| Paquete | **pnpm** |

- Escaneo histórico al arrancar (últimos 5000 bloques)
- Monitoreo en tiempo real vía polling cada 12s
- Detecta trabajo mediante el selector `work(bytes32,bytes)` en el `Sequencer`
- Tests unitarios para `WorkDetector`, `JobMonitor` y notificadores

📍 [`wonderland-challenge/`](./wonderland-challenge)

---

## Cómo explorar

Cada challenge tiene su propio README con instrucciones detalladas de setup, arquitectura y uso.

```bash
# Ej: correr el monitor blockchain
cd wonderland-challenge
pnpm install
pnpm dev
```
