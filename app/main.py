from fastapi import FastAPI
from app.models import Base
# from app.database import engine
from app.routers.v1.employee import router as employee_router
from app.rate_limiter import rate_limiter_middleware

app = FastAPI(title="Employee Search API", version="1.0.0")

# Middleware for rate limiting
app.middleware("http")(rate_limiter_middleware)

# Versioned route
app.include_router(employee_router, prefix="/api/v1")

# Create DB tables
# Base.metadata.create_all(bind=engine)
