from fastapi import APIRouter
from starlette.responses import JSONResponse
from app.api.controllers.ping_controller import ping_router
from app.api.controllers.items_controller import items_router

api_router = APIRouter(
    default_response_class=JSONResponse,
)
api_router.include_router(ping_router, tags=["ping"])
api_router.include_router(items_router, tags=["items"])