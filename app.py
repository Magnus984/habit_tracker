from schemas.schema import Base
from config.db import engine
from fastapi import FastAPI
from config.config import settings
from functools import lru_cache

#Create schema
Base.metadata.create_all(engine)

app = FastAPI(title=settings.app_name)

