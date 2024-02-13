from pprint import pprint
import asyncio
from aiohttp import ClientSession
from loguru import logger

from config import HEADERS
from utils import get_all_categories




async def main():
    async with ClientSession(headers=HEADERS) as session:
        catalog = await get_all_categories(session)



asyncio.run(main())
