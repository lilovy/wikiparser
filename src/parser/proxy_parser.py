from lxml import html
import requests
from config import (
    proxy_url,
    ip,
    port,
    protocol,
    )

def proxy_list(
    url: str = proxy_url,
    ip: str = ip,
    port: str = port,
    protocol: str = protocol,
    ) -> list[tuple[str, str]]:

    resp = requests.get(url)
    tree = html.fromstring(resp.content)

    ip = tree.xpath(ip)
    port = tree.xpath(port)
    protocol = tree.xpath(protocol)

    proxy = [(f'{i}:{port[n]}', protocol[n]) for n, i in enumerate(ip)]
    
    return proxy