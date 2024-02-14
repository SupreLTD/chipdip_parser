from dataclasses import dataclass


@dataclass
class Item:
    name: str
    count: str
    price: str
    wholesale_price: str
    manufacturer: str
