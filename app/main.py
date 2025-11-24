from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.routers import navigation, status, auth, categories, cards
from app.config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    # Optional: Run seed here if we wanted, but better to use CLI command
    yield
    # Shutdown

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Templates
templates = Jinja2Templates(directory="app/templates")

# Include Routers
app.include_router(navigation.router, prefix="/api", tags=["navigation"])
app.include_router(status.router, prefix="/api", tags=["status"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(cards.router, prefix="/api/cards", tags=["cards"])

# Root Endpoint serving HTML
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    # Vue-based admin console fetches /api/categories and /api/cards by itself
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
