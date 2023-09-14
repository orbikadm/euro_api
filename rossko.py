import os

from dotenv import load_dotenv
from zeep import Client, Settings

from classes import Part
from exceptions import RosskoApiException

load_dotenv()

API_URL_GET_ORDERS = 'http://api.rossko.ru/service/v2.1/GetOrders'
ROSSKO_API_KEY1 = os.getenv('ROSSKO_API_KEY1')
ROSSKO_API_KEY2 = os.getenv('ROSSKO_API_KEY2')


def get_parts_rossko() -> list[Part]:
    """Функция получает список заказов через API."""
    parts_list = []
    try:
        settings = Settings(strict=False, xml_huge_tree=True)
        client = Client(API_URL_GET_ORDERS, settings=settings)
        order_list = client.service.GetOrders(
            KEY1=ROSSKO_API_KEY1,
            KEY2=ROSSKO_API_KEY2,
            type=4,
            limit=100
        ).OrdersList.Order
    except Exception as error:
        raise RosskoApiException({error})
    
    for order in order_list:
        supplier = 'Rossko'
        orderid = order.id
        created_date = order.created_date
        detail = order.detail
        delivery_address = detail.delivery_address
        parts = order.parts.part
        for part in parts:
            status = part.status
            if status == 7: #  фильтрация отмененных заказов
                part_number = part.partnumber
                name = part.name
                brand = part.brand
                price = part.price
                count = part.count
                newpart = Part(
                    orderid=orderid, created_date=created_date, status=status,
                    delivery_address=delivery_address, part_number=part_number,
                    name=name, brand=brand, price=price, count=count,
                    supplier=supplier)
                parts_list.append(newpart)
    return parts_list
