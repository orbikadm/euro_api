import datetime
from settings import DATETIME_FORMAT

created_time = '27.12.2023 13:49:35'
format = '%d.%m.%Y %H:%M:%S' #%Y-%m-%d_%H-%M-%S

berg_time = '2020-03-19T04:23:56+03:00'
berg_format = '%Y-%m-%dT%H:%M:%S+03:00'
nado = '%d.%m.%Y %H:%M:%S'

first = datetime.datetime.now().strftime(DATETIME_FORMAT)
# datetime.strptime(date, "%b %d %Y %I:%M%p")
to_bd = datetime.datetime.strptime(created_time, format)

berg_dt = datetime.datetime.strptime(berg_time, berg_format)
print(type(berg_dt))
print(berg_dt)
berg_to_return = datetime.datetime.strftime(DATETIME_FORMAT)


print(type(berg_to_return))
print(berg_to_return)


API_URL_GET_ORDERS = 'http://api.rossko.ru/service/v2.1/GetOrders'