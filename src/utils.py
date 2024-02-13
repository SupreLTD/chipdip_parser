from typing import List

from aiohttp import ClientSession
from loguru import logger
from bs4 import BeautifulSoup


async def get_response_text(session: ClientSession, url: str) -> str:
    async with session.get(url) as response:
        logger.info(response.status)
        return await response.text()


async def get_catalog(session: ClientSession) -> List[str]:
    data = await get_response_text(session, 'https://www.chipdip.ru/catalog')
    soup = BeautifulSoup(data, 'lxml').find_all('li', class_='catalog__item')
    links = ['https://www.chipdip.ru' + i.find('a')['href'] for i in soup]
    return links

async def get_categories(session: ClientSession, url: str) -> List[str]:
    data = await get_response_text(session, url)
    soup = BeautifulSoup(data, 'lxml')


