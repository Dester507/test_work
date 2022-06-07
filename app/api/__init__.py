from fastapi import APIRouter

from .endpoints import (
    users,
    folders,
    files
)


router = APIRouter()
router.include_router(users.router, tags=["users"])
router.include_router(folders.router, tags=["folders"])
router.include_router(files.router, tags=["files"])
