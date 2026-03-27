from fastapi import APIRouter
from app.api.v1.auth import router as authRouter
from app.api.v1.tasks import router as taskRouter
router = APIRouter()

router.include_router(authRouter, prefix="/auth", tags=["Auth"])
router.include_router(taskRouter,prefix="/tasks",tags=["Tasks"])