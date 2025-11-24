from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.config import get_settings
from app.core.security import get_password_hash
from app.database import create_db_and_tables, engine
from app.models import User
from app.routers import navigation, status, auth, categories, cards, users, configs

settings = get_settings()


def ensure_default_admin():
    with Session(engine) as session:
        username = settings.INITIAL_ADMIN_USERNAME
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            admin_user = User(
                username=username,
                hashed_password=get_password_hash(settings.INITIAL_ADMIN_PASSWORD),
                is_superuser=True,
                is_active=True,
            )
            session.add(admin_user)
            session.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    ensure_default_admin()
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
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(configs.router, prefix="/api/configs", tags=["configs"])

# Root Endpoint serving HTML
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    # Vue-based admin console fetches /api/categories and /api/cards by itself
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "initial_admin": settings.INITIAL_ADMIN_USERNAME}
    )

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
