from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
URL_DATABASE = f"mysql+pymysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

print("==============================================================", URL_DATABASE)
engine = create_engine(URL_DATABASE, pool_size=10, max_overflow=30)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()