from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.api.controllers.invoices_controller import invoices_router
from app.api.controllers.items_controller import items_router
from app.api.controllers.ping_controller import ping_router

api_router = APIRouter(
    default_response_class=JSONResponse,
)
api_router.include_router(ping_router, tags=["ping"])
api_router.include_router(items_router, tags=["items"])
api_router.include_router(invoices_router, tags=["invoices"])
