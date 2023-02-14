from lxml import html
import requests
from socket import gethostbyname, gethostname
gethostbyname(gethostname())


def proxy_list():

    link = "https://free-proxy-list.net/"
    resp = requests.get(link)
    tree = html.fromstring(resp.content)

    elem = tree.xpath("""//*[@id='list']/div/div[2]/div/table/tbody/tr[*]/td[1]/text()""")
    elem2 = tree.xpath("//*[@id='list']/div/div[2]/div/table/tbody/tr[*]/td[2]/text()")
    elem3 = tree.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr[*]/td[7]/text()')


    proxy = [f'{i}:{elem2[n]}' for n, i in enumerate(elem)]
    
    return proxy
