from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Category, NavigationCard, SiteConfig
from app.config import get_settings

router = APIRouter()
settings = get_settings()


def _ensure_query_placeholder(url: str) -> str:
    if not url:
        return "https://www.google.com/search?q={query}"
    if "{query}" in url:
        return url
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}q={{query}}"

@router.get("/navigation")
def get_navigation_data(session: Session = Depends(get_session)):
    # Fetch Categories (ordered)
    categories = session.exec(select(Category).order_by(Category.order)).all()
    
    # Fetch Configs
    configs = session.exec(select(SiteConfig)).all()
    config_dict = {c.key: c.value for c in configs}
    
    # Construct Menu Items
    menu_items = []
    sections = []
    
    for cat in categories:
        # Menu Item
        menu_items.append({
            "id": cat.slug,
            "label": cat.label,
            "icon": cat.icon,
            "href": "#",
            "active": cat.active
        })
        
        # Section with Cards
        # Efficiently fetching cards for this category (N+1 problem here but fine for small scale)
        # For better performance, we could join or fetch all cards and map in memory.
        # Let's use the relationship.
        cards = sorted(cat.cards, key=lambda x: x.order)
        
        card_list = []
        for card in cards:
            card_list.append({
                "title": card.title,
                "subtitle": card.subtitle,
                "description": card.description,
                "icon": card.icon,
                "iconBgClass": card.icon_bg_class,
                "iconColorClass": card.icon_color_class,
                "href": card.href
            })
            
        sections.append({
            "id": cat.slug,
            "type": "grid",
            "title": cat.label,
            "cards": card_list
        })

    # Construct Final JSON
    return {
        "branding": {
            "icon": config_dict.get("branding_icon", "hub"),
            "title": config_dict.get("branding_title", "个人导航网站")
        },
        "sidebar": {
            "menuItems": menu_items,
            "status": {
                "indicator": {
                    "icon": "circle",
                    "colorClass": "text-green-500",
                    "text": "状态: 正常",
                    "tooltip": "所有系统运行正常"
                },
                "refresh": {
                    "icon": "sync",
                    "tooltip": "刚刚更新"
                }
            }
        },
        "header": {
            "links": [
                {
                    "label": "主站",
                    "href": "/"
                }
            ]
        },
        "hero": {
            "searchPlaceholder": config_dict.get("hero_search_placeholder", "搜索工具、资源..."),
            "searchEngine": {
                "name": config_dict.get("search_engine_name", "Google"),
                "url": _ensure_query_placeholder(
                    config_dict.get("search_engine_url", settings.GOOGLE_SEARCH_URL)
                )
            }
        },
        "sections": sections
    }
