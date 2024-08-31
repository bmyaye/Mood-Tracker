import datetime

import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field 
import bcrypt


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    username: str = pydantic.Field(json_schema_extra=dict(example="username"))
    email: str = pydantic.Field(json_schema_extra=dict(example="user@email.local"))
    first_name: str = pydantic.Field(json_schema_extra=dict(example="Firstname"))
    last_name: str = pydantic.Field(json_schema_extra=dict(example="Lastname"))
    
class User(BaseUser):
    id: int
    last_login_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None
    )
    register_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None
    )
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    scope: str
    issued_at: datetime.datetime
    user_id: int


class RegisteredUser(BaseUser):
    password: str = pydantic.Field(json_schema_extra=dict(example="password"))

class Login(BaseModel):
    email: EmailStr
    password: str
class UpdatedUser(BaseUser):
    pass

class ChangedPassword(BaseModel):
    current_password: str
    new_password: str
    
class DeleteUserRequest(BaseModel):
    password: str

class DBUser(BaseUser, SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)

    password: str

    register_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    last_login_date: datetime.datetime | None = Field(default=None)

    async def get_encrypted_password(self, plain_password):
        return bcrypt.hashpw(
            plain_password.encode("utf-8"), salt=bcrypt.gensalt()
        ).decode("utf-8")

    async def set_password(self, plain_password):
        self.password = await self.get_encrypted_password(plain_password)

    async def verify_password(self, plain_password):
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), self.password.encode("utf-8")
        )
