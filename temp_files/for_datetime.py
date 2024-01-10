import datetime
from settings import DATETIME_FORMAT

created_time = '27.12.2023 13:49:35'
format = '%d.%m.%Y %H:%M:%S' #%Y-%m-%d_%H-%M-%S


first = datetime.datetime.now().strftime(DATETIME_FORMAT)
# datetime.strptime(date, "%b %d %Y %I:%M%p")
to_bd = datetime.datetime.strptime(created_time, format)


print(type(first))
print(first)
print(type(to_bd))
print(to_bd)
