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
SessionLocal = sessionmaker(autocommit=True, bind=engine)
Base = declarative_base()


def connect():
    try:
        db = SessionLocal()
        # this is where the "work" happens!
        yield db
        # always commit changes!
        db.commit()
    except Exception as e:
        # if any kind of exception occurs, rollback transaction
        db.rollback()
        raise
    finally:
        db.close()


def Db():
    return next(connect())
