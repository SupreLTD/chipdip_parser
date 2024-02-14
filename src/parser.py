from asyncio import sleep

from aiohttp import ClientSession
from loguru import logger
from random import shuffle
from tqdm import tqdm

from config import HEADERS
from utils import get_catalog, get_categories, get_items, to_csv
from db_client import save_data, cleaner_products_table


async def main():
    logger.info('Start parsing...')
    await cleaner_products_table()
    async with ClientSession(headers=HEADERS) as session:
        logger.info('Parsing catalog')
        catalog = await get_catalog(session)
        shuffle(catalog)
        categories = []
        for cat in catalog:
            logger.info(f'Parsing category {cat}')
            categories.extend(await get_categories(session, cat))
            await sleep(0.1)
        categories = [f"{i.replace('catalog-show', 'catalog')}?ps=x3&page=" for i in categories]
        shuffle(categories)
        logger.info('Parsing items...')
        for category in tqdm(categories):
            products = await get_items(session, category)
            if products:
                await save_data(products)
                logger.info(f'Saved in DB {len(products)} items')

    await to_csv()
    logger.info('Finished parsing.')



