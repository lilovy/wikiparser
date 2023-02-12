from src.parser.parse_wiki_data import parse_wiki, parse_wiki_page, load_data
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from lxml import html, etree


async def main():

    tasks = []
    for word in load_data():
        task = asyncio.create_task(
            parse_wiki_page(
                word=word,
                )
                )

        tasks.append(task)

    await asyncio.gather(*tasks)

async def parse():
    body = await resp.text()
    soup = BeautifulSoup(body, 'html.parser')
    dom = etree.HTML(str(soup))

async def

async def content():
    try:
        if isinstance(self._values[0], str):
            yield self.__join(self._values)        
        else:
            for n, i in enumerate(self._values, start=1):
                self._sense = i.xpath(f"""{self._pathin.format(n=n)}""")
                yield self._sense
    except:
        await []


async def scrape(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            await parse()

            values = dom.xpath("""//*[@id="mw-content-text"]/div[1]/ol[1]/li""")



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
