from datetime import datetime
import requests

from models import Order
from settings import BERG_API_URL, BERG_KEY, BERG_TIME


statuses = {
    1: 'Обнулен',
    3: 'Снят с резерва',
    663: 'Задержка поставки'
}


def get_parts_berg() -> list[Order]:
    "Получаем список отмененных заказов от Берга."
    result: list[Order] = []
    url = BERG_API_URL + BERG_KEY
    response = requests.get(url).json()
    orders_list = response.get('orders')

    for order in orders_list:
        supplier = 'Berg'
        orderid = str(order.get('id'))
        created_date = order.get('created_at')
        created_date = datetime.strptime(created_date, BERG_TIME)
        delivery_address = order.get('shipment_address')
        items = order.get('items')
        for item in items:
            part_status = item.get('state').get('id')

            if part_status in tuple(statuses.keys()):
                status = statuses.get(part_status)
                result.append(
                    Order(
                        order_id=orderid,
                        article=item.get('resource').get('article'),
                        supplier=supplier,
                        cancel_time=datetime.now(),
                        created_date=created_date,
                        delivery_address=delivery_address,
                        name=item.get('resource').get('name'),
                        brand=item.get('resource').get('brand').get('name'),
                        price=str(item.get('price')),
                        count=str(item.get('quantity')),
                        status=status,
                    )
                )

    return result
