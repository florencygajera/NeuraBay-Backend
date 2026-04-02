from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import require_admin
from app.db.session import get_db
from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut
from app.services.contact_service import create_contact_message, list_contact_messages, get_contact_message, update_contact_message
from app.utils.helpers import standard_response

router = APIRouter()


@router.post("/", response_model=dict)
async def create_contact(obj_in: ContactCreate, db: AsyncSession = Depends(get_db)):
    contact = await create_contact_message(db, obj_in)
    return standard_response(ContactOut.model_validate(contact))


@router.get("/", response_model=dict)
async def list_contacts(limit: int = 20, offset: int = 0, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    contacts = await list_contact_messages(db, limit, offset)
    return standard_response([ContactOut.model_validate(c) for c in contacts], meta={"limit": limit, "offset": offset})


@router.get("/{contact_id}", response_model=dict)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    contact = await get_contact_message(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return standard_response(ContactOut.model_validate(contact))


@router.put("/{contact_id}", response_model=dict)
async def update_contact(contact_id: int, obj_in: ContactUpdate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    contact = await get_contact_message(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    updated = await update_contact_message(db, contact, obj_in)
    return standard_response(ContactOut.model_validate(updated))
