from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models import SiteConfig
from app.core.deps import get_current_superuser
from app.config import get_settings

router = APIRouter()

settings = get_settings()

SEARCH_PLACEHOLDER_KEY = "hero_search_placeholder"
SEARCH_ENGINE_NAME_KEY = "search_engine_name"
SEARCH_ENGINE_URL_KEY = "search_engine_url"
BRANDING_TITLE_KEY = "branding_title"
BRANDING_ICON_KEY = "branding_icon"
DEFAULT_PLACEHOLDER = "搜索工具、资源..."
DEFAULT_ENGINE_NAME = "Google"
DEFAULT_ENGINE_URL = settings.GOOGLE_SEARCH_URL or "https://www.google.com/search?q={query}"
DEFAULT_BRANDING_TITLE = settings.APP_NAME or "个人导航网站"
DEFAULT_BRANDING_ICON = "hub"


class SearchConfigResponse(BaseModel):
    placeholder: str
    engine_name: str
    engine_url: str


class SearchConfigUpdate(BaseModel):
    placeholder: Optional[str] = None
    engine_name: Optional[str] = None
    engine_url: Optional[str] = None


class BrandingConfigResponse(BaseModel):
    title: str
    icon: str


class BrandingConfigUpdate(BaseModel):
    title: Optional[str] = None
    icon: Optional[str] = None


def _get_config_value(session: Session, key: str) -> Optional[SiteConfig]:
    return session.exec(select(SiteConfig).where(SiteConfig.key == key)).first()


def _upsert_config(session: Session, key: str, value: str) -> SiteConfig:
    config = _get_config_value(session, key)
    if config:
        config.value = value
    else:
        config = SiteConfig(key=key, value=value)
        session.add(config)
    session.add(config)
    return config


def _build_search_config(session: Session) -> SearchConfigResponse:
    placeholder = _get_config_value(session, SEARCH_PLACEHOLDER_KEY)
    engine_name = _get_config_value(session, SEARCH_ENGINE_NAME_KEY)
    engine_url = _get_config_value(session, SEARCH_ENGINE_URL_KEY)

    return SearchConfigResponse(
        placeholder=placeholder.value if placeholder else DEFAULT_PLACEHOLDER,
        engine_name=engine_name.value if engine_name else DEFAULT_ENGINE_NAME,
        engine_url=engine_url.value if engine_url else DEFAULT_ENGINE_URL,
    )


def _build_branding_config(session: Session) -> BrandingConfigResponse:
    title = _get_config_value(session, BRANDING_TITLE_KEY)
    icon = _get_config_value(session, BRANDING_ICON_KEY)

    return BrandingConfigResponse(
        title=title.value if title else DEFAULT_BRANDING_TITLE,
        icon=icon.value if icon else DEFAULT_BRANDING_ICON,
    )


@router.get("/search", response_model=SearchConfigResponse)
def get_search_config(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_superuser)
):
    return _build_search_config(session)


@router.put("/search", response_model=SearchConfigResponse)
def update_search_config(
    payload: SearchConfigUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_superuser)
):
    data = payload.model_dump(exclude_unset=True)

    if "placeholder" in data:
        _upsert_config(session, SEARCH_PLACEHOLDER_KEY, data["placeholder"])
    if "engine_name" in data:
        _upsert_config(session, SEARCH_ENGINE_NAME_KEY, data["engine_name"])
    if "engine_url" in data:
        _upsert_config(session, SEARCH_ENGINE_URL_KEY, data["engine_url"])

    session.commit()

    return _build_search_config(session)


@router.get("/branding", response_model=BrandingConfigResponse)
def get_branding_config(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_superuser)
):
    return _build_branding_config(session)


@router.put("/branding", response_model=BrandingConfigResponse)
def update_branding_config(
    payload: BrandingConfigUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_superuser)
):
    data = payload.model_dump(exclude_unset=True)

    if "title" in data:
        _upsert_config(session, BRANDING_TITLE_KEY, data["title"])
    if "icon" in data:
        _upsert_config(session, BRANDING_ICON_KEY, data["icon"])

    session.commit()

    return _build_branding_config(session)
