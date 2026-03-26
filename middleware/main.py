from fastapi import FastAPI
from middleware.api.routes import router as api_router
from middleware.config.env import settings

# Initialize the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for Proactive Network Capacity Management POC",
    version="1.0.0"
)

# Register routes with a /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")

# health check endpoint
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "Server is up and running smoothly."}
