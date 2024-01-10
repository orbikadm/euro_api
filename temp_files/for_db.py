from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import declarative_base, Session

import datetime

format = '%d.%m.%Y %H:%M:%S'
Base = declarative_base()

class Order(Base):
    __tablename__ = 'order'
    uniq_id = Column(String, primary_key=True)
    supplier = Column(String)
    created_date = Column(DateTime)
    delivery_address = Column(Text)
    name = Column(String)
    brand = Column(String)
    price = Column(String)
    count = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return self.uniq_id


engine = create_engine('sqlite:///testsqlite.db')
Base.metadata.create_all(engine)
session = Session(engine)



parts_in_db = session.query(Order).all()
print(parts_in_db)


rossko_mock_response = [
    ((90305610, 'LT-1150'), 'Rossko', '27.12.2023 13:49:35', 'Биробиджан г, Еврейская Аобл, Комбайностроителей, 38 к 3, Автосервис ЕВРОТЕХ', 'Фильтр АКПП', 'LYNXauto', '3062.00', 1, 2),
    ((90290585, '1520831U0B'), 'Rossko', '27.12.2023 11:13:03', 'Биробиджан г, Еврейская Аобл, Комбайностроителей, 38 к 3, Автосервис ЕВРОТЕХ', 'Фильтр масляный', 'Nissan', '631.08', 1, 2),
    ((90284425, 'SI-1061'), 'Rossko', '27.12.2023 07:46:06', 'Биробиджан г, Еврейская Аобл, Комбайностроителей, 38 к 3, Автосервис ЕВРОТЕХ', 'Рычаг подвески | зад прав |', 'SUFIX', '2015.00', 1, 2),
    ((90284425, 'C8592'), 'Rossko', '27.12.2023 07:46:06', 'Биробиджан г, Еврейская Аобл, Комбайностроителей, 38 к 3, Автосервис ЕВРОТЕХ', 'Втулка стабилизатора | перед лев |', 'LYNXauto', '353.00', 1, 2),
    ((90284425, 'C7293LR'), 'Rossko', '27.12.2023 07:46:06', 'Биробиджан г, Еврейская Аобл, Комбайностроителей, 38 к 3, Автосервис ЕВРОТЕХ', 'Стойка стабилизатора | перед прав/лев |', 'LYNXauto', '799.00', 2, 2),
    ((90284425, 'C8593'), 'Rossko', '27.12.2023 07:46:06', 'Биробиджан г, Еврейская Аобл, Комбайностроителей, 38 к 3, Автосервис ЕВРОТЕХ', 'Втулка стабилизатора | перед прав |', 'LYNXauto', '393.00', 1, 2)
]

for part in rossko_mock_response:
    uniq_id = str(part[0])

    order = Order(
        uniq_id=uniq_id,
        supplier=part[1],
        created_date=datetime.datetime.strptime(part[2], format),
        delivery_address=part[3],
        name=part[4],
        brand=part[5],
        price=part[6],
        count=part[7],
        status=part[8],
    )


    count = session.query(Order).get(uniq_id)
    print(count)
    if not count:
        session.add(order)
        session.commit()
