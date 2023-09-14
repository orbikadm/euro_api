from dataclasses import dataclass


@dataclass
class Part:
    supplier: str
    orderid: int
    created_date: str
    delivery_address: str
    status: int
    part_number: str
    name: str
    brand: str
    price: float
    count: int