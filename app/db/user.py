from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.hashing import Hasher
from app.models.user import User
from app.schemas.user import UserCreate

# Check if user is active or not


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = Hasher.get_password_hash(user.password)
    db_user = models.user.User(
        email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def update_user(db: Session, user_id: int, user: schemas.user.UserUpdate):
#     db.query(User).filter(User.id == user_id).update(
#         {"is_active": user.is_active}, synchronize_session='fetch')
#     db.commit()
#     return db.query(User).filter(User.id == user_id).first()
