from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from moodtracker.models import get_session
from moodtracker.models.users import DBUser, RegisteredUser,ChangedPassword,DeleteUserRequest
from pydantic import BaseModel
import datetime


from .. import deps
from .. import models

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Create User
@router.post("/")
async def create_user(
    user: RegisteredUser,
    session: AsyncSession = Depends(get_session)
    )->  models.User:
    query = select(DBUser).where(DBUser.username == user.username)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    db_user = DBUser(**user.dict())
    await db_user.set_password(user.password)  # Encrypt password before saving
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)



    await session.commit()  # Commit the Point to generate the point_id

    return db_user

@router.get("/me")
def get_me(current_user: models.User = Depends(deps.get_current_user)) -> models.User:
    return current_user

# Read User
# @router.get("/{user_id}")
# async def get_user(
#     user_id: int,
#     session: Annotated[AsyncSession, Depends(models.get_session)],
#     current_user: models.User = Depends(deps.get_current_user),
# ) -> models.User:
#     user = await session.get(models.DBUser, user_id)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="Not found this user",
#         )
#     return user

# Update User
@router.put("/edit-profile/")
async def update_user(
    user_update: models.UpdatedUser,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user),
)-> models.User:
    user = await session.get(DBUser, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.first_name is not None:
        user.first_name = user_update.first_name
    if user_update.last_name is not None:
        user.last_name = user_update.last_name
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

# Change Password
@router.put("/change-password/")
async def change_password(
    request: ChangedPassword,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user),
):
    user = await session.get(DBUser, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not await user.verify_password(request.current_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    if await user.verify_password(request.new_password):
        raise HTTPException(status_code=400, detail="New password must be different from the current password")

    await user.set_password(request.new_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"message": "Password updated successfully"}

# Delete User
@router.delete("/delete/")
async def delete_user(
    request: DeleteUserRequest,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user),
):
    user = await session.get(DBUser, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not await user.verify_password(request.password):
        raise HTTPException(status_code=400, detail="Password is incorrect")

    await session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully"}