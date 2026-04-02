from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, require_admin
from app.db.session import get_db
from app.schemas.user import UserOut, UserUpdate
from app.services.user_service import list_user_items, get_user_item, update_user_item, delete_user_item
from app.utils.helpers import standard_response

router = APIRouter()


@router.get("/me", response_model=dict)
async def read_me(current_user=Depends(get_current_user)):
    return standard_response(UserOut.model_validate(current_user))


@router.get("/", response_model=dict)
async def list_users(limit: int = 20, offset: int = 0, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    users = await list_user_items(db, limit, offset)
    return standard_response([UserOut.model_validate(u) for u in users], meta={"limit": limit, "offset": offset})


@router.get("/{user_id}", response_model=dict)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    user = await get_user_item(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return standard_response(UserOut.model_validate(user))


@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: int, obj_in: UserUpdate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    user = await get_user_item(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated = await update_user_item(db, user, obj_in)
    return standard_response(UserOut.model_validate(updated))


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    user = await get_user_item(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    deleted = await delete_user_item(db, user)
    return standard_response({"id": deleted.id, "deleted": True})
