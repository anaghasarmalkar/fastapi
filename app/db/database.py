from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import *


SQLALCHEMY_DATABASE_URL = "sqlite:///app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# We need to have an independent database session/connection (SessionLocal) per request, use the same session through all the request and then close it after the request is finished.
# new session will be created for the next request.


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)


# def seed_data():
#     db_session = SessionLocal()

#     admin_role = RoomUserRole(name="admin")
#     member_role = RoomUserRole(name="member")

#     db_session.add(admin_role)
#     db_session.add(member_role)
#     db_session.commit()
