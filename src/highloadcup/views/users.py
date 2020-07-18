from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field, parse_obj_as

from ..models.users import User, Visit, Location

router = APIRouter()

from highloadcup.views.visits import VisitModel


class UserModel(BaseModel):
    id: int = Field(..., ge=0)
    email: str = Field(..., max_length=100)
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    gender: str = Field(..., regex=r"(m|f)")
    birth_date: int = Field(...)

    class Config:
        orm_mode = True


class UpdateUserModel(BaseModel):
    email: str = Field(None, max_length=100)
    first_name: str = Field(None, max_length=50)
    last_name: str = Field(None, max_length=50)
    gender: str = Field(None, regex=r"(m|f)")
    birth_date: int = Field(None)

    class Config:
        orm_mode = True


@router.get("/users/{pk}", response_model=UserModel)
async def get_user(pk: int):
    user = await User.get_or_404(pk)
    return user.to_dict()


@router.post("/users/new")
async def create_user(user: UserModel):
    await User.create(**user.dict())
    return {}


@router.post("/users/{pk}")
async def update_user(pk: int, user: UpdateUserModel):
    await User.update.values(**user.dict(exclude_unset=True)).where(User.id == pk).gino.status()
    return {}


@router.get("/users/{pk}/visits")
async def get_visits(pk: int,
                     from_date: Optional[int] = Query(None, alias="fromDate"),
                     to_date: Optional[int] = Query(None, alias="toDate"),
                     country: Optional[str] = Query(None, max_length=50),
                     to_distance: Optional[int] = Query(None, alias="toDistance", ge=0)):
    v = Visit.query
    if country or to_distance:
        v = Visit.join(Location).select()

    v = v.where(Visit.user == pk)
    if from_date:
        v = v.where(Visit.visited_at > from_date)
    if to_date:
        v = v.where(Visit.visited_at < to_date)
    if country:
        v = v.where(Location.country == country)
    if to_distance:
        v = v.where(Location.distance < to_distance)

    visits = await v.gino.all()

    return [VisitModel.from_orm(visit).dict() for visit in visits]


def init_app(app):
    app.include_router(router)
