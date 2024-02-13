from asyncio import sleep
from pprint import pprint
import asyncio
from aiohttp import ClientSession
from loguru import logger

from config import HEADERS
from utils import get_catalog, get_categories


async def main():
    async with ClientSession(headers=HEADERS) as session:
        catalog = await get_catalog(session)
        for cat in catalog:
            res = await get_categories(session, cat)
            await sleep(1)
            print(res)



asyncio.run(main())
