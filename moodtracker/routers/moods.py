from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Annotated
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models
from .. import deps


router = APIRouter()


@router.get("")
async def read_moods(
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.MoodList:
    result = await session.exec(select(models.DBMood))
    moods = result.all()

    return models.MoodList.from_orm(dict(moods=moods, page_size=0, page=0, size_per_page=0))


@router.post("")
async def create_mood(
    mood: models.CreatedMood,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> models.MoodList:
    data = mood.dict()
    dbmood = models.DBMood.parse_obj(data)
    dbmood.user_id = current_user.id
    session.add(dbmood)
    await session.commit()
    await session.refresh(dbmood)

    return models.Mood.from_orm(dbmood)


@router.put("")
async def update_mood(
    mood: models.UpdatedMood,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
) -> models.Mood:
    data = mood.dict()
    dbmood = models.DBMood.parse_obj(data)
    dbmood.user_id = current_user.id
    session.add(dbmood)
    await session.commit()
    await session.refresh(dbmood)

    return models.Mood.from_orm(dbmood)