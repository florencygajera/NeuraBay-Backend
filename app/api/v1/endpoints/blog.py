from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import require_admin
from app.db.session import get_db
from app.schemas.blog import BlogCreate, BlogUpdate, BlogOut
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.schemas.tag import TagCreate, TagUpdate, TagOut
from app.services.blog_service import create_blog_post, update_blog_post, list_blog_posts, get_blog_post, delete_blog_post
from app.services.taxonomy_service import (
    create_category_item,
    update_category_item,
    list_category_items,
    get_category_item,
    delete_category_item,
    create_tag_item,
    update_tag_item,
    list_tag_items,
    get_tag_item,
    delete_tag_item,
)
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


@router.get("/categories", response_model=dict)
async def list_categories(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    categories = await list_category_items(db, limit, offset)
    return standard_response([CategoryOut.model_validate(c) for c in categories], meta={"limit": limit, "offset": offset})


@router.post("/categories", response_model=dict)
async def create_category(obj_in: CategoryCreate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    category = await create_category_item(db, obj_in)
    return standard_response(CategoryOut.model_validate(category))


@router.put("/categories/{category_id}", response_model=dict)
async def update_category(category_id: int, obj_in: CategoryUpdate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    category = await get_category_item(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    updated = await update_category_item(db, category, obj_in)
    return standard_response(CategoryOut.model_validate(updated))


@router.delete("/categories/{category_id}", response_model=dict)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    category = await get_category_item(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    deleted = await delete_category_item(db, category)
    return standard_response({"id": deleted.id, "deleted": True})


@router.get("/tags", response_model=dict)
async def list_tags(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    tags = await list_tag_items(db, limit, offset)
    return standard_response([TagOut.model_validate(t) for t in tags], meta={"limit": limit, "offset": offset})


@router.post("/tags", response_model=dict)
async def create_tag(obj_in: TagCreate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    tag = await create_tag_item(db, obj_in)
    return standard_response(TagOut.model_validate(tag))


@router.put("/tags/{tag_id}", response_model=dict)
async def update_tag(tag_id: int, obj_in: TagUpdate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    tag = await get_tag_item(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    updated = await update_tag_item(db, tag, obj_in)
    return standard_response(TagOut.model_validate(updated))


@router.delete("/tags/{tag_id}", response_model=dict)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    tag = await get_tag_item(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    deleted = await delete_tag_item(db, tag)
    return standard_response({"id": deleted.id, "deleted": True})
