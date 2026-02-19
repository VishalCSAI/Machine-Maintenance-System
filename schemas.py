from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MachineBase(BaseModel):
    name: str = Field(..., description="Human readable machine name")
    location: Optional[str] = Field(None, description="Physical location of the machine")
    description: Optional[str] = Field(None, description="Short description of the machine")
    is_active: bool = Field(True, description="Whether machine is currently active")


class MachineCreate(MachineBase):
    pass


class MachineUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class MachineInDB(MachineBase):
    id: str


class MaintenanceTaskBase(BaseModel):
    machine_id: str
    title: str
    description: Optional[str] = None
    due_date: datetime
    status: str = Field("scheduled", description="scheduled | in_progress | completed | cancelled")


class MaintenanceTaskCreate(MaintenanceTaskBase):
    pass


class MaintenanceTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None


class MaintenanceTaskInDB(MaintenanceTaskBase):
    id: str
    created_at: datetime
    updated_at: datetime

