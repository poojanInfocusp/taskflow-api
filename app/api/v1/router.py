from fastapi import APIRouter
from app.api.v1.auth import router as authRouter

router = APIRouter()

router.include_router(authRouter, prefix="/auth", tags=["Auth"])
