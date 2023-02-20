
__author__ = "Lilovy"

import requests
from lxml import html, etree
from bs4 import BeautifulSoup
from random import choice
from src.parser.proxy_parser import proxy_list



class Parse:
    def __init__(
        self, 
        url: str,
        xpath: str = None,
        content: str = None,
        proxy: bool = False,
        ) -> None:

        self._url = url
        self._page = ''
        self._path = xpath
        self._pathin = content
        self._proxies = proxy


    def _set_page(self, page: str) -> None:
        self._page = self._url + page

    def __proxy(self):

        proxies = self._proxies
        if proxies:
            proxies = choice(proxies)
            proxy = proxies[0]
            protocol = 'http'
            if proxies[1] == 'yes':
                protocol = 'https'

        proxy = {
            protocol: proxy,
        }
        return proxy

    def __response(self):
        headers = (
            {'User-Agent':'Safari/537.36',
            'Accept-Language':'en-US, en;q=0.5'}
            )
        
        try:
            r = requests.get(
                self._page, 
                headers=headers,
                )

            while r.status_code == requests.codes.too_many:
                print('wait...')
                if self._proxies:
                    r = requests.get(
                        self._page,
                        headers=headers,
                        proxies=self.__proxy(),
                    )
                else:
                    r = requests.get(
                        self._page,
                        headers=headers,
                        timeout=50,
                    )

            return r

        except Exception as e:
            raise e


    def _parse(self) -> None:


        self._resp = self.__response()
        
        self._soup = BeautifulSoup(self._resp.content, 'html.parser')
        # self._tree = html.fromstring(self._resp.content)
        self._dom = etree.HTML(str(self._soup))

    def __xpath(self) -> None:
        self._values: list = self._dom.xpath(f"""{self._path}""")
        # self._values: list = self._tree.xpath(f"""{self._path}""")

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

    def request(self, page: str):
        """
        make request from the page
        """
        self._set_page(page)
        self._parse()
        print(self._resp, page)

    def parse(self) -> list[str]:
        """
        return data from the page
        """
        self.__xpath()
        return self.__represent()
    
    def return_html(self):
        ...
        return str(self._soup)

    def xpath(self, path: str) -> None:
        self._path = path

    def content(self, path: str) -> None:
        self._pathin = path

    def proxy(self, proxy: list) -> None:
        self._proxies = proxy

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
