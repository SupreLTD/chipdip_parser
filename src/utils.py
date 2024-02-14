from asyncio import sleep
from pprint import pprint
from typing import List

from aiohttp import ClientSession
from aiohttp.abc import HTTPException
from loguru import logger
from bs4 import BeautifulSoup
from tenacity import retry

from models import Item


@retry
async def get_response_text(session: ClientSession, url: str) -> str | None:
    async with session.get(url) as response:
        if response.status != 200:
            if response.status == 404:
                return
            else:
                logger.info(f'{response.status} | {url}')
                raise ValueError()
        # logger.info(response.status)
        return await response.text()


async def get_catalog(session: ClientSession) -> List[str]:
    data = await get_response_text(session, 'https://www.chipdip.ru/catalog')
    soup = BeautifulSoup(data, 'lxml').find_all('li', class_='catalog__item')
    links = ['https://www.chipdip.ru' + i.find('a')['href'] for i in soup]
    return links


async def get_categories(session: ClientSession, url: str) -> List[str]:
    data = await get_response_text(session, url)
    soup = BeautifulSoup(data, 'lxml')
    elements = soup.find('div', class_='no-visited clear catalog')
    if elements:
        categories = elements.find_all('a', class_='link')
        links = ['https://www.chipdip.ru' + i['href'] for i in categories]
        return links
    else:
        return [url]


async def get_items(session: ClientSession, url: str) -> List[Item]:
    result = []
    page = 1
    while True:
        data = await get_response_text(session, f'{url}{page}')
        if not data:
            break
        items = get_items_from_html(data)
        # print(items)
        if not items:
            break
        result.extend(items)
        page += 1
        await sleep(0.05)

    return result


def get_items_from_html(text: str) -> List[Item | None]:
    result = []
    soup = BeautifulSoup(text, 'lxml')
    table = soup.find('table', class_='itemlist itemlist_main')
    if table:
        items = table.find_all('tr', class_='with-hover')
        for item in items:
            count = item.find('span', class_='item__avail item__avail_available nw')
            if count:
                count = count.text
            else:
                continue
            name = item.find('a').text
            manufacturer = item.find('span', class_='itemlist_pval').text
            price = item.find('span', class_='price price-main').text.replace('\xa0', ' ')
            wholesale_price = item.find('div', class_='addprice-w').text.strip().replace('\xa0', ' ')

            result.append(Item(
                name=name,
                count=count,
                price=price,
                wholesale_price=wholesale_price,
                manufacturer=manufacturer
            ))
    return result
