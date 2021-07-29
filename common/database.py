import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import config

db_engine = create_engine(
    config.DB_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base = declarative_base()

if 'sqlite' in config.DB_URL:
    db_url = config.DB_URL
elif 'mysql' in config.DB_URL:
    db_url = config.DB_URL.replace('+pymysql', '')
else:
    raise Exception('db url error')

db = databases.Database(db_url)
