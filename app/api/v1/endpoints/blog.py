from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import require_admin
from app.db.session import get_db
from app.schemas.blog import BlogCreate, BlogUpdate, BlogOut
from app.services.blog_service import create_blog_post, update_blog_post, list_blog_posts, get_blog_post, delete_blog_post
from app.utils.helpers import standard_response

router = APIRouter()


@router.get("/", response_model=dict)
async def list_blogs(
    limit: int = 20,
    offset: int = 0,
    search: str | None = None,
    category_id: int | None = None,
    tag_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    blogs = await list_blog_posts(db, limit, offset, search, category_id, tag_id)
    return standard_response([BlogOut.model_validate(b) for b in blogs], meta={"limit": limit, "offset": offset})


@router.post("/", response_model=dict)
async def create_blog(obj_in: BlogCreate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    blog = await create_blog_post(db, obj_in, author_id=admin.id)
    return standard_response(BlogOut.model_validate(blog))


@router.get("/{blog_id}", response_model=dict)
async def get_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await get_blog_post(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return standard_response(BlogOut.model_validate(blog))


@router.put("/{blog_id}", response_model=dict)
async def update_blog(blog_id: int, obj_in: BlogUpdate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    blog = await get_blog_post(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    updated = await update_blog_post(db, blog, obj_in)
    return standard_response(BlogOut.model_validate(updated))


@router.delete("/{blog_id}", response_model=dict)
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    blog = await get_blog_post(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    deleted = await delete_blog_post(db, blog)
    return standard_response({"id": deleted.id, "deleted": True})
