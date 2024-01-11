import datetime
import requests

from settings import BERG_API_URL, BERG_KEY, BERG_TIME


statuses = {
    1: 'Обнулен',
    3: 'Снят с резерва',
    663: 'Задержка поставки'
}


def get_parts_berg() -> list:
    "Получаем список отмененных заказов от Берга."
    parts_list = []
    url = BERG_API_URL + BERG_KEY
    result = requests.get(url).json()
    orders_list = result.get('orders')

    for order in orders_list:
        supplier = 'Berg'
        orderid = str(order.get('id'))
        created_date = order.get('created_at')
        created_date = datetime.datetime.strptime(created_date, BERG_TIME)
        delivery_address = order.get('shipment_address')
        items = order.get('items')
        for item in items:
            status = item.get('state').get('id')
            article = item.get('resource').get('article')
            name = item.get('resource').get('name')
            brand = item.get('resource').get('brand').get('name')
            price = str(item.get('price'))
            count = str(item.get('quantity'))

            if status in tuple(statuses.keys()):  #  фильтрация отмененных заказов
                status = statuses.get(status)
                parts_list.append(
                    (
                        orderid, article, supplier, created_date,
                        delivery_address, name, brand, price, count, str(status)
                    )
                )

    return parts_list
