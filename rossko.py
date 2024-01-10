from zeep import Client, Settings
from exceptions import RosskoApiException

from settings import ROSSKO_API_KEY1, ROSSKO_API_KEY2, API_URL_GET_ORDERS


def get_parts_rossko() -> list[tuple[str]]:
    """Получаем список отмененных заказов от Росско."""
    parts_list: list[tuple[str]] = []
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
        supplier: str = 'Rossko'
        orderid: str = str(order.id)
        created_date: str = order.created_date
        detail = order.detail
        delivery_address: str = detail.delivery_address
        parts = order.parts.part
        for num, part in enumerate(parts):
            status: str = part.status
            if num == 7:  #  фильтрация отмененных заказов (7 - отмененные)
                status = 'Отменен'
                part_number: str = part.partnumber
                name: str = part.name
                brand: str = part.brand
                price: str = part.price
                count: str = str(part.count)
                parts_list.append(
                    (
                        orderid, part_number, supplier, created_date,
                        delivery_address, name, brand, price, count, status
                    )
                )

    return parts_list
