from datetime import datetime

from zeep import Client, Settings
from exceptions import RosskoApiException

from models import Order
from settings import (
    ROSSKO_API_KEY1, ROSSKO_API_KEY2, API_URL_GET_ORDERS, DATETIME_FORMAT
)


statuses = {
    7: 'Отменен',
}

delivery_adresses = {
    'Биробиджан, улица Миллера, 26': 'Миллера',
    'Биробиджан г, Еврейская Аобл, Широкая ул, 15': 'Широкая',
    '680009, край.Хабаровский, г.Хабаровск, проспект 60-летия Октября, дом № 170, корпус А': 'Хабаровск',
    'Хабаровск, Проспект 60 лет Октября, 170 а': 'Хабаровск',
    'Хабаровск, Проспект 60 лет Октября, 170 а': 'ДСМ',
}


def get_parts_rossko() -> list[tuple[str]]:
    """Получаем список отмененных заказов от Росско."""
    parts_list: list[tuple[str]] = []
    try:
        settings = Settings(strict=False, xml_huge_tree=True)
        client = Client(API_URL_GET_ORDERS, settings=settings)
        order_list = client.service.GetOrders(
            KEY1=ROSSKO_API_KEY1,
            KEY2=ROSSKO_API_KEY2,
            limit=100
        ).OrdersList.Order
    except Exception as error:
        raise RosskoApiException({error})

    for order in order_list:
        supplier: str = 'Rossko'
        orderid: str = str(order.id)
        created_date: str = order.created_date
        created_date = datetime.strptime(created_date, DATETIME_FORMAT)
        detail = order.detail
        delivery_address: str = detail.delivery_address
        if delivery_address is None:
            delivery_address = 'Самовывоз'
        parts = order.parts.part
        for part in parts:
            status = part.status
            if status in tuple(statuses.keys()):
                parts_list.append(
                    Order(
                        order_id=orderid,
                        article=part.partnumber,
                        supplier=supplier,
                        cancel_time=datetime.now(),
                        created_date=created_date,
                        delivery_address=delivery_address,
                        name=part.name,
                        brand=part.brand,
                        price=part.price,
                        count=str(part.count),
                        status=statuses.get(status),
                    )
                )

    return parts_list
