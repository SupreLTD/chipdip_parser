from dataclasses import asdict

from aiotinydb import AIOTinyDB

from models import Item


async def save_data(data: list[Item]) -> None:
    data = [asdict(i) for i in data]
    async with AIOTinyDB('db.json') as db:
        table = db.table('products')
        table.insert_multiple(data)


async def cleaner_products_table() -> None:
    async with AIOTinyDB('db.json') as db:
        table = db.table('products')
        table.truncate()
