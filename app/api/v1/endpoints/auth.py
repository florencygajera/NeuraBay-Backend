from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.user import UserCreate, Token, TokenRefresh
from app.services.auth_service import register_user
from app.crud.user import get_user_by_email
from app.utils.helpers import standard_response

router = APIRouter()


@router.post("/register", response_model=dict)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await register_user(db, user_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return standard_response({"id": user.id, "email": user.email})


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(subject=user.email, role=user.role)
    refresh_token = create_refresh_token(subject=user.email)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
async def refresh_token(payload: TokenRefresh, db: AsyncSession = Depends(get_db)):
    try:
        from jose import jwt
        from app.core.config import settings

        token_payload = jwt.decode(payload.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if token_payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        email = token_payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(subject=email, role=user.role)
    refresh_token = create_refresh_token(subject=email)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=dict)
async def me(current_user=Depends(get_current_user)):
    return standard_response({"id": current_user.id, "email": current_user.email, "role": current_user.role})
