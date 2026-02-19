## Machine Maintenance Scheduler (FastAPI + MongoDB + React)

This project is a small **e2e machine maintenance scheduling web app** built with:

- **Backend**: Python, FastAPI, MongoDB (via Motor)
- **Frontend**: React + Vite

It lets you:

- **View machines** and their basic information
- **Schedule new maintenance tasks** for a selected machine
- **View upcoming / existing tasks** for a machine
- **Update task status** (scheduled, in_progress, completed, cancelled)

---

### 1. Project structure

- **backend/**
  - `requirements.txt` – Python dependencies
  - `app/main.py` – FastAPI app entrypoint
  - `app/database.py` – MongoDB connection
  - `app/schemas.py` – Pydantic models (machines, maintenance tasks)
  - `app/routers_machines.py` – API routes for machines and tasks
- **frontend/**
  - `package.json` – Frontend dependencies and scripts
  - `vite.config.mts` – Vite config with proxy to backend
  - `index.html` – Root HTML
  - `src/main.jsx` – React entrypoint
  - `src/App.jsx` – Main UI (machines + tasks)
  - `src/styles.css` – Minimal modern UI styling

---

### 2. Prerequisites

- **Python 3.10+**
- **Node.js 18+** and **npm** (or pnpm/yarn)
- **MongoDB** running locally (default URI `mongodb://localhost:27017`)

You can override the MongoDB connection via environment variables:

- `MONGODB_URI` – e.g. `mongodb://localhost:27017`
- `MONGODB_DB_NAME` – defaults to `maintenance_db`

Create a `.env` file in `backend/` if you want custom values:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=maintenance_db
```

---

### 3. Backend setup (FastAPI)

From the project root (`untitled folder 2`):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with docs at `http://localhost:8000/docs`.

Key endpoints:

- `GET /health` – Simple health check
- `GET /machines/` – List machines
- `POST /machines/` – Create machine
- `GET /machines/{machine_id}` – Get machine details
- `PUT /machines/{machine_id}` – Update machine
- `DELETE /machines/{machine_id}` – Delete machine
- `GET /tasks/?machine_id=...` – List tasks (optionally by machine)
- `POST /tasks/` – Create task
- `PUT /tasks/{task_id}` – Update task (e.g. status)
- `DELETE /tasks/{task_id}` – Delete task

---

### 4. Frontend setup (React + Vite)

In a new terminal, from the project root:

```bash
cd frontend
npm install
npm run dev
```

The React app will run at `http://localhost:5173`.

Vite is configured to **proxy `/api` to the FastAPI server** on `http://localhost:8000`, so the frontend talks to the backend using relative paths like `/api/machines/` and `/api/tasks/`.

---

### 5. Basic usage flow

1. Start **MongoDB** (e.g. `mongod`).
2. Start the **FastAPI backend** (`uvicorn app.main:app --reload --port 8000`).
3. Start the **React frontend** (`npm run dev` in `frontend`).
4. Open `http://localhost:5173` in your browser.
5. In the UI:
   - Add one or more **machines** with name, location, description.
   - Select a machine in the left panel.
   - Create **maintenance tasks** with a title, description, and due date/time.
   - Update task status as work progresses.

---

### 6. Next steps / ideas

- Add authentication and role-based access (e.g. supervisors vs technicians).
- Add recurring maintenance schedules and reminders.
- Attach documents or checklists to tasks.
- Add filtering by upcoming / overdue tasks and richer dashboards.

This scaffold is intentionally lightweight so you can extend it to match your exact requirements. 


