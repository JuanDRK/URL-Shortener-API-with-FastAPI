from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import url

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="API para acortar URLs con estadísticas",
    version="1.0.0"
)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "url-shortener-api"}


app.include_router(url.router, prefix="/api", tags=["URLs"])