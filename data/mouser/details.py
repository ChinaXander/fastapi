"""
@Time           :2022/6/8
@author         :XDS
@Description    :
"""
from data.database import Base
from sqlalchemy import Column, Integer, String


class Details(Base):
    __tablename__ = "mouser_detail_all"
    id = Column(Integer, primary_key=True)
    model = Column(String)
    brand = Column(String)
    category = Column(String)
    attributes = Column(String)
    picpath = Column(String)
    pdfpath = Column(String)
    description = Column(String)
    origin = Column(String)
