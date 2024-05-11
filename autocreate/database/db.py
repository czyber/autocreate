import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "example.db")
engine = create_engine('sqlite:///{}'.format(db_path), echo=True)

Session = sessionmaker(bind=engine)

