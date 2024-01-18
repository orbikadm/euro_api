from berg import get_parts_berg
from rossko import get_parts_rossko


def get_orders(rossko=False, berg=False):
    part_list = []
    if rossko:
        part_list.extend(get_parts_rossko())
    if berg:
        part_list.extend(get_parts_berg())
    return part_list
