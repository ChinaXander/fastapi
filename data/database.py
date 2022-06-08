"""
@Time           :2022/6/7
@author         :XDS
@Description    :
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import settings

SQLALCHEY_DATABASE_URI: str = settings.mysql_url

engine = create_engine(SQLALCHEY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Db = SessionLocal()
