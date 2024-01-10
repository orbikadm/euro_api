import requests

from settings import BERG_API_URL, BERG_KEY


statuses = {
    '1': 'Обнулен',
    '3': 'Снят с резерва',
    '663': 'Задержка поставки'
}


def get_parts_berg() -> list:
    "Получаем список отмененных заказов от Берга."
    parts_list = []
    url = BERG_API_URL + BERG_KEY
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

            if status in (1, 3, 663):  #  фильтрация отмененных заказов
                status = statuses[status]
                parts_list.append(
                    (
                        orderid, part_number, supplier, created_date,
                        delivery_address, name, brand, price, count, status
                    )
                )
    # print('ORDER_LIST', orders_list)
    # print('PART_LIST', parts_list)

    return parts_list


# get_parts_berg()
