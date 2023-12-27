# Версия Python 3.9
### Формат сохранения в БД отмененных заказов:
(orderid, part_number), created_date, status,
delivery_address, name, brand, price, count, supplier

где (orderid, part_number) - uniq_id (Уникальный id, он же ключ для поиска)

### Выставить настройки уровня логгирования перед запуском