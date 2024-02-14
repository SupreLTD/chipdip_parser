from asyncio import sleep
from pprint import pprint
import asyncio
from aiohttp import ClientSession
from loguru import logger
from random import shuffle

from config import HEADERS
from utils import get_catalog, get_categories, get_items

logger.add('lols.log', level='DEBUG')


async def main():
    async with ClientSession(headers=HEADERS) as session:
        catalog = await get_catalog(session)
        shuffle(catalog)
        categories = []
        for cat in catalog:
            categories.extend(await get_categories(session, cat))
            # break
            await sleep(0.05)
        categories = [f"{i.replace('catalog-show', 'catalog')}?ps=x3&page=" for i in categories]
        shuffle(categories)
        for category in categories:
            logger.info(category)
            products = await get_items(session, category)
            print(products)



asyncio.run(main())
