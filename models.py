from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Session

from settings import DATABASE


Base = declarative_base()


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    order_id = Column(String)
    article = Column(String)
    supplier = Column(String)
    cancel_time = Column(DateTime)
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
