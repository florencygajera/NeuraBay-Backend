from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import require_admin, get_current_user
from app.db.session import get_db
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceOut
from app.services.service_service import create_service_item, update_service_item, list_service_items, get_service_item, delete_service_item
from app.services.ai_service import chatbot_reply
from app.utils.helpers import standard_response

router = APIRouter()


@router.get("/", response_model=dict)
async def list_services(limit: int = 20, offset: int = 0, db: AsyncSession = Depends(get_db)):
    services = await list_service_items(db, limit, offset)
    return standard_response([ServiceOut.model_validate(s) for s in services], meta={"limit": limit, "offset": offset})


@router.post("/", response_model=dict)
async def create_service(
    obj_in: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin),
):
    service = await create_service_item(db, obj_in, created_by=admin.id)
    return standard_response(ServiceOut.model_validate(service))


@router.get("/{service_id}", response_model=dict)
async def get_service(service_id: int, db: AsyncSession = Depends(get_db)):
    service = await get_service_item(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return standard_response(ServiceOut.model_validate(service))


@router.put("/{service_id}", response_model=dict)
async def update_service(
    service_id: int,
    obj_in: ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin),
):
    service = await get_service_item(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    updated = await update_service_item(db, service, obj_in)
    return standard_response(ServiceOut.model_validate(updated))


@router.delete("/{service_id}", response_model=dict)
async def delete_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin),
):
    service = await get_service_item(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    deleted = await delete_service_item(db, service)
    return standard_response({"id": deleted.id, "deleted": True})


@router.post("/ai/chat", response_model=dict)
async def ai_chat(message: str, current_user=Depends(get_current_user)):
    reply = await chatbot_reply(message)
    return standard_response(reply)
