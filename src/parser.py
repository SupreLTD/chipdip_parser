from asyncio import sleep
from pprint import pprint
import asyncio
from aiohttp import ClientSession
from loguru import logger
from random import shuffle

from config import HEADERS
from utils import get_catalog, get_categories

logger.add('lols.log', level='DEBUG')


async def main():
    async with ClientSession(headers=HEADERS) as session:
        catalog = await get_catalog(session)
        shuffle(catalog)
        categories = []
        for cat in catalog:
            categories.extend(await get_categories(session, cat))
            await sleep(0.05)
        categories = [i.replace('catalog-show', 'catalog')+'?ps=x3&page=' for i in categories]
        pprint(categories)


asyncio.run(main())
