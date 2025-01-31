from schemas.schema import Base
from config.db import engine
from fastapi import FastAPI
from config.config import settings
from api.v1.routes import api_router

#Create schema
Base.metadata.create_all(engine)

app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix="/api/v1")
