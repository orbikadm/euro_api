import requests
import json


key = '5062031b80982cd3535a8e5e8e76a1a2e01f1a4226e6ce38becd868c9a22febb'
url = 'https://api.berg.ru/ordering/states/active?key=5062031b80982cd3535a8e5e8e76a1a2e01f1a4226e6ce38becd868c9a22febb'
result = requests.get(url).json()

orders_list = result.get('orders')
with open('berg_response.txt', 'w', encoding='utf-8') as file:
    file.write(str(orders_list) + '\n')

for order in orders_list:
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

        with open('berg_items.txt', 'a', encoding='utf-8') as file:
            file.write('Номер заказа: ' + str(orderid) + '\n')
            file.write('Дата заказа: ' + str(created_date) + '\n')
            file.write('Адресс доставки: ' + str(delivery_address) + '\n')
            file.write('Статус: ' + str(status) + '\n')
            file.write('Артикул: ' + str(part_number) + '\n')
            file.write('Наименование: ' + str(name) + '\n')
            file.write('Бренд: ' + str(brand) + '\n')
            file.write('Цена: ' + str(price) + '\n')
            file.write('Количество: ' + str(count) + '\n')
            file.write('\n')





# print(data)