import json
import os
from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import Category, NavigationCard, SiteConfig, User

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def seed_data():
    create_db_and_tables()
    
    json_path = os.path.join("docs", "prototype", "data", "navigation.json")
    if not os.path.exists(json_path):
        print(f"Warning: Data file not found at {json_path}")
        return

    data = load_json_data(json_path)
    
    with Session(engine) as session:
        # Check if data already exists
        existing_cats = session.exec(select(Category)).first()
        if existing_cats:
            print("Data already exists, skipping seed.")
            return

        print("Seeding database...")
        
        # Map slug to category object for easier card insertion
        slug_to_category = {}

        # 1. Seed Categories (from sidebar.menuItems)
        menu_items = data.get("sidebar", {}).get("menuItems", [])
        for idx, item in enumerate(menu_items):
            category = Category(
                slug=item["id"],
                label=item["label"],
                icon=item["icon"],
                order=idx,
                active=item.get("active", False)
            )
            session.add(category)
            session.flush() # flush to get ID
            session.refresh(category)
            slug_to_category[category.slug] = category
        
        # 2. Seed Cards (from sections)
        sections = data.get("sections", [])
        for section in sections:
            cat_slug = section["id"]
            category = slug_to_category.get(cat_slug)
            
            if not category:
                print(f"Warning: Section with id '{cat_slug}' has no matching category menu item.")
                continue

            cards = section.get("cards", [])
            for idx, card_data in enumerate(cards):
                card = NavigationCard(
                    category_id=category.id,
                    title=card_data["title"],
                    subtitle=card_data.get("subtitle"),
                    description=card_data["description"],
                    icon=card_data["icon"],
                    icon_bg_class=card_data["iconBgClass"],
                    icon_color_class=card_data["iconColorClass"],
                    href=card_data["href"],
                    order=idx
                )
                session.add(card)

        # 3. Seed Configs (Branding, etc.)
        branding = data.get("branding", {})
        if branding:
             session.add(SiteConfig(key="branding_title", value=branding.get("title", "Nav")))
             session.add(SiteConfig(key="branding_icon", value=branding.get("icon", "hub")))
        
        hero = data.get("hero", {})
        if hero:
            session.add(SiteConfig(key="hero_search_placeholder", value=hero.get("searchPlaceholder", "Search...")))

        session.commit()
        
        # 4. Seed Admin User
        existing_user = session.exec(select(User).where(User.username == "admin")).first()
        if not existing_user:
            from app.core.security import get_password_hash
            admin_user = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                is_superuser=True
            )
            session.add(admin_user)
            session.commit()
            print("Created admin user: admin / admin123")
        
        print("Seeding complete.")

if __name__ == "__main__":
    seed_data()
