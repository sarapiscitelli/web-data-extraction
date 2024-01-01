from fastapi import APIRouter

from .endpoints import web_extraction

api_router = APIRouter()
api_router.include_router(web_extraction.router, prefix="/web-extraction", tags=["web-extraction"])
