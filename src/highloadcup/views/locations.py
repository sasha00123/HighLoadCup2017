import calendar
from datetime import datetime
from typing import Optional

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Query
from highloadcup.models import db
from pydantic import BaseModel, Field
from sqlalchemy import func

from ..models.users import Location, User, Visit

router = APIRouter()


class LocationModel(BaseModel):
    id: int = Field(..., ge=0)
    place: str = Field(...)
    country: str = Field(..., max_length=50)
    city: str = Field(..., max_length=50)
    distance: int = Field(..., ge=0)


class UpdateLocationModel(BaseModel):
    place: str = Field(None)
    country: str = Field(None, max_length=50)
    city: str = Field(None, max_length=50)
    distance: int = Field(None, ge=0)


@router.get("/locations/{pk}")
async def get_location(pk: int):
    location = await Location.get_or_404(pk)
    return location.to_dict()


@router.post("/locations/new")
async def create_location(location: LocationModel):
    return await Location.create(**location.dict())


@router.post("/locations/{pk}")
async def update_location(pk: int, location: UpdateLocationModel):
    await Location.update().values(**location.dict(exclude_unset=True)).where(Location.id == pk).gino.status()
    return {}


@router.get("/locations/{pk}/avg")
async def get_average_mark(pk: int,
                           from_date: Optional[int] = Query(None, alias="fromDate"),
                           to_date: Optional[int] = Query(None, alias="toDate"),
                           from_age: Optional[int] = Query(None, alias="fromAge"),
                           to_age: Optional[int] = Query(None, alias="toAge"),
                           gender: Optional[str] = Query(None, regex="(m|f)")):
    _ = await Location.get_or_404(pk)

    v = db.func.avg(Visit.mark).select()
    if from_age or to_age or gender:
        v = v.select_from(User.join(Visit))

    v = v.where(Visit.location == pk)
    if from_date:
        v = v.where(Visit.visited_at > from_date)
    if to_date:
        v = v.where(Visit.visited_at < to_date)

    if from_age or to_age:
        now = datetime.now() - relativedelta(years=from_age)
        timestamp = calendar.timegm(now.timetuple())

        if from_age:
            v = v.where(User.birth_date > timestamp)
        if to_age:
            v = v.where(User.birth_date < timestamp)

    if gender:
        v = v.where(User.gender == gender)

    return {'avg': await v.gino.scalar() or 0}


def init_app(app):
    app.include_router(router)
