from fastapi import APIRouter
from app.routers.api.users import users
from app.routers.api.auth import auth
from app.routers.api.rooms import rooms

router = APIRouter(prefix="/api", tags=["Api"])

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(rooms.router)
