from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, alerts, traffic, websocket
from app.services.sniffer import sniffer_service
from app.api.v1.websocket import manager

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend API and Real-Time WebSocket server for Network Attack Detection System."
)

# CORS Middleware (allowing React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(alerts.router, prefix=f"{settings.API_V1_STR}/alerts", tags=["Alerts"])
app.include_router(traffic.router, prefix=f"{settings.API_V1_STR}/traffic", tags=["Traffic"])
app.include_router(websocket.router, tags=["WebSockets"])

def handle_sniffer_alert(alert_data):
    """Callback triggered whenever sniffer + ML engine detects suspicious flow."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(manager.broadcast(alert_data), loop)
    except Exception as e:
        print(f"Error forwarding alert to websocket: {e}")

@app.on_event("startup")
async def startup_event():
    # Create DB tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Register sniffer callback
    sniffer_service.register_callback(handle_sniffer_alert)
    print("Application startup complete. Ready for real-time traffic detection.")

@app.on_event("shutdown")
async def shutdown_event():
    sniffer_service.stop()
    print("Application shutdown complete.")

@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "status": "Online",
        "docs": "/docs"
    }
