from zeep import Client, Settings
from classes import Part
from exceptions import RosskoApiException

from constants import ROSSKO_API_KEY1, ROSSKO_API_KEY2, API_URL_GET_ORDERS


def get_parts_rossko() -> list[tuple]:
    """Функция получает список заказов через API."""
    parts_list: list[tuple] = []
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
            status: str = part.status
            if status == 7:  #  фильтрация отмененных заказов
                part_number: str = part.partnumber
                name: str = part.name
                brand: str = part.brand
                price: float = part.price
                count: str = part.count
                uniq_id: tuple[str] = (orderid, part_number)
                parts_list.append(
                    (
                        uniq_id, supplier, created_date, delivery_address, name,
                        brand, price, count, status
                    )
                )
    return parts_list
