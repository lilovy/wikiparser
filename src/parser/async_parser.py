
""" 

   create by lilovy 

"""

import asyncio, httpx
from lxml import html, etree
from bs4 import BeautifulSoup


class Parse:
    def __init__(
        self, 
        url: str,
        ) -> None:

        self._url = url
        self._page = ''        
        self._path = None
        self._pathin = self._path


    def _set_page(self, page: str) -> None:
        self._page = self._url + page

    async def __get_page(self, url: str) -> str:
        _xpath_headers = ({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
            })
        async with httpx.AsyncClient(
            # headers=_xpath_headers,
            # timeout=30,
            ) as client:
            return await client.get(url)
            

    async def _parse(self) -> None:

        # self._resp = await requests.get(self._page, headers=_xpath_headers)
        self._resp = await self.__get_page(self._page)
        print(self._resp, self._page)
        self._soup = BeautifulSoup(self._resp.text, 'lxml')
        self._dom = etree.HTML(str(self._soup))

    def __xpath(self) -> None:
        self._values: list = self._dom.xpath(f"""{self._path}""")

    def _content(self) -> str:
        try:
            if isinstance(self._values[0], str):
                yield self.__join(self._values)        
            else:
                for n, i in enumerate(self._values, start=1):
                    self._sense = i.xpath(f"""{self._pathin.format(n=n)}""")
                    yield self._sense
        except:
            return []

    def __join(self, param: str) -> str:
        __join = ''
        for i in param:
            __join += i.replace('\xa0', ' ')
        return __join

    def __represent(self) -> list:
        self._result = []
        for i in self._content():
            if len(i) > 0:
                self._result.append(self.__join(i))
        return self._result

    async def request(self, page: str) -> None:
        """
        make request from the page
        """
        self._set_page(page)
        await self._parse()

    def parse(self) -> list[str]:
        """
        return data from the page
        """
        self.__xpath()
        return self.__represent()

    def xpath(self, path: str) -> None:
        self._path = path

    def content(self, path: str) -> None:
        if path:
            self._pathin = path

    def storage(self) -> list:
        data = []
        for i in self._content():
            data.append(i)

        return data

url = 'https://ru.wiktionary.org/wiki/'

values = """//*[@id="mw-content-text"]/div[1]/ol[1]/li"""

pth ="""//*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/text() | 
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/a/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/a/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/span/a/span/text()
    """


words = ['абзац', 'туземец']

if __name__ == '__main__':
    wik = Parse(url)

    for l in words:
        wik.request(l)
        wik.xpath(values)
        wik.content(pth)
        print(l)
        print('')

        print(wik.parse())
        wik.xpath('//*[@id="mw-content-text"]/div[1]/p[2]/a[1]/text()')
        print(wik.parse())
        # print(wik.storage())
