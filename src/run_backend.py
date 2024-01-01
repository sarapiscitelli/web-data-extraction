import uvicorn
import os


if __name__ == "__main__":
    from backend.main import app

    uvicorn.run(
        app=app, host=os.environ["SCRAPER_BACKEND_HOST"], port=int(os.environ["SCRAPER_BACKEND_PORT"])
    )
