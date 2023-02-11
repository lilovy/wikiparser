
""" 

   create by lilovy 

"""

import requests
from lxml import html, etree
from bs4 import BeautifulSoup


class Parse:
    def __init__(self, url: str) -> None:
        self._url = url
        self._page = ''        
        self._path = None
        self._pathin = self._path


    def _set_page(self, page: str) -> None:
        self._page = self._url + page

    def _parse(self) -> None:
        _xpath_headers = ({'User-Agent':
                          'Safari/537.36',\
                          'Accept-Language':
                          'en-US, en;q=0.5'})

        self._resp = requests.get(self._page, headers=_xpath_headers)
        self._soup = BeautifulSoup(self._resp.content, 'html.parser')
        self._dom = etree.HTML(str(self._soup))

    def __xpath(self) -> None:
        self._values = self._dom.xpath(f"""{self._path}""")

    def _content(self) -> str:
        if isinstance(self._values[0], str):
            yield self.__join(self._values)        
        else:
            for n, i in enumerate(self._values, start=1):
                self._sense = i.xpath(f"""{self._pathin.format(n=n)}""")
                yield self._sense

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

    def parse(self, page: str) -> list:
        """
        return data from the page
        """
        self._set_page(page)
        self._parse()
        self.__xpath()
        return self.__represent()

    def xpath(self, path: str) -> None:
        self._path = path

    def content(self, path: str) -> None:
        if path:
            self._pathin = path

url = 'https://ru.wiktionary.org/wiki/'

values = """//*[@id="mw-content-text"]/div[1]/ol[1]/li"""

pth ="""//*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/text() | 
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/a/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/a/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/span/a/span/text()"""


words = ['абзац', 'туземец']

if __name__ == '__main__':
    wik = Parse(url)
    wik.xpath(values)
    wik.content(pth)

    for l in words:
        print(l)
        print('')

        print(wik.parse(f"{l}"))
