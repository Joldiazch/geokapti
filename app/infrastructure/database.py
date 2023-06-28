from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from sqlmodel import SQLModel
from app.api.schemas import Location, User
import json

DATABASE_URL = "postgresql://postgres:postgres@db/geokapti_database"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_db():
    SQLModel.metadata.create_all(engine)


def drop_db():
    SQLModel.metadata.drop_all(engine)


def populate_tables():
    session = SessionLocal()

    if not session.query(User).count() > 0 and not session.query(User).count() > 0:
        hashed_password = pwd_context.hash('admin')
        new_user = User(username='admin', password=hashed_password)
        session.add(new_user)

        with open(r'app/infrastructure/locations.json', 'r') as f:
            locations = json.load(f)

        for location_data in locations:
            location_data |= {'user': new_user}
            location = Location(**location_data)
            session.add(location)

        try:
            session.commit()
            print("The location table has been successfully populated.")
        except IntegrityError:
            session.rollback()
            print("Error. The location table has not been populated.")
        finally:
            session.close()