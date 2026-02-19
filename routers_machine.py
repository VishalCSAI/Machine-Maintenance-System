from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from .database import get_collection
from . import schemas


router = APIRouter(prefix="/machines", tags=["machines"])


def _obj_to_machine(doc) -> schemas.MachineInDB:
    return schemas.MachineInDB(
        id=str(doc["_id"]),
        name=doc["name"],
        location=doc.get("location"),
        description=doc.get("description"),
        is_active=doc.get("is_active", True),
    )


@router.get("/", response_model=List[schemas.MachineInDB])
async def list_machines():
    coll = get_collection("machines")
    docs = await coll.find({}).to_list(length=1000)
    return [_obj_to_machine(doc) for doc in docs]


@router.post("/", response_model=schemas.MachineInDB, status_code=status.HTTP_201_CREATED)
async def create_machine(machine: schemas.MachineCreate):
    coll = get_collection("machines")
    result = await coll.insert_one(machine.model_dump())
    doc = await coll.find_one({"_id": result.inserted_id})
    return _obj_to_machine(doc)


@router.get("/{machine_id}", response_model=schemas.MachineInDB)
async def get_machine(machine_id: str):
    coll = get_collection("machines")
    try:
        oid = ObjectId(machine_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Machine not found")

    doc = await coll.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Machine not found")
    return _obj_to_machine(doc)


@router.put("/{machine_id}", response_model=schemas.MachineInDB)
async def update_machine(machine_id: str, update: schemas.MachineUpdate):
    coll = get_collection("machines")
    try:
        oid = ObjectId(machine_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Machine not found")

    payload = {k: v for k, v in update.model_dict(exclude_unset=True).items()}
    if not payload:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await coll.find_one_and_update(
        {"_id": oid},
        {"$set": payload},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Machine not found")
    return _obj_to_machine(result)


@router.delete("/{machine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_machine(machine_id: str):
    coll = get_collection("machines")
    try:
        oid = ObjectId(machine_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Machine not found")

    res = await coll.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Machine not found")


tasks_router = APIRouter(prefix="/tasks", tags=["maintenance_tasks"])


def _obj_to_task(doc) -> schemas.MaintenanceTaskInDB:
    return schemas.MaintenanceTaskInDB(
        id=str(doc["_id"]),
        machine_id=str(doc["machine_id"]),
        title=doc["title"],
        description=doc.get("description"),
        due_date=doc["due_date"],
        status=doc["status"],
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )


@tasks_router.get("/", response_model=List[schemas.MaintenanceTaskInDB])
async def list_tasks(machine_id: str | None = None, status_filter: str | None = None):
    coll = get_collection("maintenance_tasks")
    query = {}
    if machine_id:
        try:
            query["machine_id"] = ObjectId(machine_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid machine id")
    if status_filter:
        query["status"] = status_filter

    docs = await coll.find(query).sort("due_date").to_list(length=1000)
    return [_obj_to_task(doc) for doc in docs]


@tasks_router.post("/", response_model=schemas.MaintenanceTaskInDB, status_code=status.HTTP_201_CREATED)
async def create_task(task: schemas.MaintenanceTaskCreate):
    coll = get_collection("maintenance_tasks")
    try:
        machine_oid = ObjectId(task.machine_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid machine id")

    now = datetime.utcnow()
    payload = task.model_dump()
    payload["machine_id"] = machine_oid
    payload["created_at"] = now
    payload["updated_at"] = now

    result = await coll.insert_one(payload)
    doc = await coll.find_one({"_id": result.inserted_id})
    return _obj_to_task(doc)


@tasks_router.put("/{task_id}", response_model=schemas.MaintenanceTaskInDB)
async def update_task(task_id: str, update: schemas.MaintenanceTaskUpdate):
    coll = get_collection("maintenance_tasks")
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")

    payload = {k: v for k, v in update.model_dict(exclude_unset=True).items()}
    if not payload:
        raise HTTPException(status_code=400, detail="No fields to update")

    payload["updated_at"] = datetime.utcnow()

    result = await coll.find_one_and_update(
        {"_id": oid},
        {"$set": payload},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return _obj_to_task(result)


@tasks_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    coll = get_collection("maintenance_tasks")
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")

    res = await coll.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

