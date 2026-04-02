from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, services, blog, contact, career, testimonials

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(blog.router, prefix="/blog", tags=["blog"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(career.router, prefix="/career", tags=["career"])
api_router.include_router(testimonials.router, prefix="/testimonials", tags=["testimonials"])
