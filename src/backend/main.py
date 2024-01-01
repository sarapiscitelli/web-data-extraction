import os
from fastapi import FastAPI

from .api.api_v1 import api_router


app = FastAPI(
    title="Web extraction", openapi_url=f"{os.getenv('SCRAPER_API_V1_STR')}/openapi.json"
)

# include all endpoint containing in api packages
app.include_router(api_router, prefix=os.getenv("SCRAPER_API_V1_STR"))
