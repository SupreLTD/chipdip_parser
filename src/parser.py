from pprint import pprint
import asyncio
from aiohttp import ClientSession
from loguru import logger

from config import HEADERS
from utils import get_catalog




async def main():
    async with ClientSession(headers=HEADERS) as session:
        catalog = await get_catalog(session)



asyncio.run(main())
