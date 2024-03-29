import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_USER = os.environ.get('DB_USER', 'omolytics')
DB_PASS = os.environ.get('DB_PASS', '')
DB_HOST = os.environ.get('DB_HOST', 'omolytics_1')
DB_NAME = os.environ.get('DB_NAME', 'omolytics')

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False,
    bind=engine
)

# TODO do we need this if we have get_db() in utils?
session = SessionLocal()