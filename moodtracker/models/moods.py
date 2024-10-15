import datetime
import pydantic

from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship


class BaseMood(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    description: str | None = None
    mood_type: str



class CreatedMood(BaseMood):
    pass


class UpdatedMood(BaseMood):
    pass


class Mood(BaseMood):
    mood_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"),
        default=None
    )


class DBMood(Mood, SQLModel, table=True):
    __tablename = "mood"
    id: Optional[int] = Field(default=None, primary_key=True)
    # user_id: int = Field(default=None, foreign_key="users.id")
    mood_date: datetime.datetime = Field(default_factory=datetime.datetime.now)


class MoodList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    moods: list[Mood]
    page: int
    page_count: int
    size_per_page: int
