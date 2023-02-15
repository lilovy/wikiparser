url = 'https://ru.wiktionary.org/wiki/'

xpath = """//*[@id="mw-content-text"]/div[1]/ol[1]/li"""

content = (
        """
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/text() | 
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/a/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/a/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/span/a/span/text()
        """
)

DB = 'words.db'

file = 'words.txt'

encoding = 'utf-8'


# proxy config

proxy_url = 'https://free-proxy-list.net/'

ip = "//*[@id='list']/div/div[2]/div/table/tbody/tr[*]/td[1]/text()"

port = "//*[@id='list']/div/div[2]/div/table/tbody/tr[*]/td[2]/text()"

protocol = "//*[@id='list']/div/div[2]/div/table/tbody/tr[*]/td[7]/text()"