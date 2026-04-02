from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import require_admin
from app.db.session import get_db
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate, TestimonialOut
from app.services.testimonial_service import create_testimonial_item, list_testimonial_items, get_testimonial_item, update_testimonial_item, delete_testimonial_item
from app.utils.helpers import standard_response

router = APIRouter()


@router.get("/", response_model=dict)
async def list_testimonials(limit: int = 20, offset: int = 0, approved_only: bool = True, db: AsyncSession = Depends(get_db)):
    testimonials = await list_testimonial_items(db, limit, offset, approved_only)
    return standard_response([TestimonialOut.model_validate(t) for t in testimonials], meta={"limit": limit, "offset": offset})


@router.post("/", response_model=dict)
async def create_testimonial(obj_in: TestimonialCreate, db: AsyncSession = Depends(get_db)):
    testimonial = await create_testimonial_item(db, obj_in)
    return standard_response(TestimonialOut.model_validate(testimonial))


@router.get("/{testimonial_id}", response_model=dict)
async def get_testimonial(testimonial_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    testimonial = await get_testimonial_item(db, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return standard_response(TestimonialOut.model_validate(testimonial))


@router.put("/{testimonial_id}", response_model=dict)
async def update_testimonial(testimonial_id: int, obj_in: TestimonialUpdate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    testimonial = await get_testimonial_item(db, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    updated = await update_testimonial_item(db, testimonial, obj_in)
    return standard_response(TestimonialOut.model_validate(updated))


@router.delete("/{testimonial_id}", response_model=dict)
async def delete_testimonial(testimonial_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    testimonial = await get_testimonial_item(db, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    deleted = await delete_testimonial_item(db, testimonial)
    return standard_response({"id": deleted.id, "deleted": True})
