from fastapi import FastAPI
from app.api.routes import api_router
import logging

logging.basicConfig(level=logging.INFO)

def create_app(**kwargs) -> FastAPI:
  app: FastAPI = FastAPI()
  app.include_router(api_router)
  return app