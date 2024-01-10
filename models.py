from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, Session

from settings import DATABASE


Base = declarative_base()


class Order(Base):
    __tablename__ = 'order'
    id = Column(String, primary_key=True)
    order_id = Column(String)
    article = Column(String)
    supplier = Column(String)
    created_date = Column(DateTime)
    delivery_address = Column(String)
    name = Column(String)
    brand = Column(String)
    price = Column(String)
    count = Column(String)
    status = Column(String)


engine = create_engine(f'sqlite:///{DATABASE}')
Base.metadata.create_all(engine)
session = Session(engine)
