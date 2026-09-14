"""FastAPI Application Main Entrypoint."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings
from src.analytics.database import db_manager
from src.data.loader import load_cleaned_data
from api.routes import schools, analytics, agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if settings.CLEANED_DATA_PATH.exists():
            df = load_cleaned_data()
            db_manager.init_database(df)
    except Exception:
        pass
    yield
    db_manager.close()

app = FastAPI(
    title="StudentIQ Welfare & Retention API",
    description="State Education Department Analytics & AI Analyst API for Mid-Day Meal, Infrastructure, and Dropout Tracking",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schools.router)
app.include_router(analytics.router)
app.include_router(agent.router)

@app.get("/", tags=["Health"])
def health():
    return {
        "status": "online",
        "system": "StudentIQ Welfare Efficacy Tracker",
        "duckdb_connected": True
    }