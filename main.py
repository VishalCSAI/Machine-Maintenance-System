from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Database
from .routers_machines import router as machines_router, tasks_router


app = FastAPI(title="Machine Maintenance Scheduler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    Database.get_db()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await Database.close()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(machines_router)
app.include_router(tasks_router)

