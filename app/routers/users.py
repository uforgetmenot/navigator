from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.core.deps import get_current_superuser
from app.core.security import get_password_hash
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/", response_model=List[UserRead])
def read_users(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_superuser)
):
    users = session.exec(select(User).order_by(User.id)).all()
    return users


@router.post("/", response_model=UserRead)
def create_user(
    user_in: UserCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_superuser)
):
    existing = session.exec(select(User).where(User.username == user_in.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = User(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_superuser)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)

    is_default_admin = user.username == settings.INITIAL_ADMIN_USERNAME

    new_username = update_data.get("username")
    if new_username and new_username != user.username:
        existing = session.exec(select(User).where(User.username == new_username)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

    if is_default_admin:
        forbidden_fields = {"username", "is_superuser", "is_active"}
        attempted = forbidden_fields.intersection(update_data.keys())
        if attempted:
            raise HTTPException(status_code=400, detail="Default admin username/role/state cannot be changed")

    if "password" in update_data:
        password = update_data.pop("password")
        if password:
            user.hashed_password = get_password_hash(password)

    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_superuser)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"ok": True}
