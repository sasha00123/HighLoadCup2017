from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..models.users import Visit

router = APIRouter()


class VisitModel(BaseModel):
    id: int = Field(..., ge=0)
    location: int = Field(..., ge=0)
    user: int = Field(..., ge=0)
    visited_at: int = Field(...)
    mark: int = Field(..., ge=1, le=5)

    class Config:
        orm_mode = True


class UpdateVisitModel(BaseModel):
    location: int = Field(None, ge=0)
    user: int = Field(None, ge=0)
    visited_at: int = Field(None)
    mark: int = Field(None, ge=1, le=5)

    class Config:
        orm_mode = True


@router.get("/visits/{pk}")
async def get_visit(pk: int):
    visit = await Visit.get_or_404(pk)
    return visit.to_dict()


@router.post("/visits/new")
async def create_visit(visit: VisitModel):
    await Visit.create(**visit.dict())
    return {}


@router.post("/visits/{pk}")
async def update_visit(pk: int, visit: UpdateVisitModel):
    await Visit.update.values(**visit.dict(exclude_unset=True)).where(Visit.id == pk).gino.status()
    return {}


def init_app(app):
    app.include_router(router)
