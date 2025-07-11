from typing import Any, Dict

from fastapi import APIRouter

ping_router = APIRouter()


@ping_router.get(
    "/ping",
    summary="ping endpoint",
    description="for testing if services are up and running!",
    response_model=None,
)
async def ping() -> Dict[str, Any]:
    """For testing servers"""
    data = {"message": "pong!", "status": 200}
    return data
