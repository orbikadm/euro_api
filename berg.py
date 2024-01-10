import os
import requests
from dotenv import load_dotenv



load_dotenv()

BERG_KEY = os.getenv('BERG_KEY')


def get_parts_berg() -> list:
    "Получаем список инстансов Part."
    parts_list = []
    url = 'https://api.berg.ru/ordering/states/active?key=' + BERG_KEY
    result = requests.get(url).json()

    orders_list = result.get('orders')

    for order in orders_list:
        supplier = 'Berg'
        orderid = order.get('id')
        created_date = order.get('created_at')
        delivery_address = order.get('shipment_address')
        items = order.get('items')
        for item in items:
            status = item.get('state').get('id')
            part_number = item.get('resource').get('article')
            name = item.get('resource').get('name')
            brand = item.get('resource').get('brand').get('name')
            price = item.get('price')
            count = item.get('quantity')

            if status == 3:  #  фильтрация отмененных заказов
                newpart = Part(
                    orderid=orderid, created_date=created_date, status=status,
                    delivery_address=delivery_address, part_number=part_number,
                    name=name, brand=brand, price=price, count=count,
                    supplier=supplier)
                parts_list.append(newpart)
    return parts_list
