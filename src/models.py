from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Item:
    name: str
    count: str
    price: str
    wholesale_price: str
    manufacturer: str
