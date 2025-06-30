from fastapi import FastAPI
from app.api import router
from app.models import Base
from app.database import engine

app = FastAPI(title="Employee Search API", version="1.0.0")
app.include_router(router)

Base.metadata.create_all(bind=engine)
