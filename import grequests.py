from lxml import html
import requests


link = "https://free-proxy-list.net/"
resp = requests.get(link)
tree = html.fromstring(resp.content)
elem = tree.xpath("//*[@id='list']/div/div[2]/div/table/tbody/tr[*]/td[1]")
elem2 = tree.xpath("//*[@id='list']/div/div[2]/div/table/tbody/tr[*]/td[2]")
elem1_2 = elem[0].text + ':' + elem2[0].text
print(elem1_2) # 95.217.84.60:8118

for i in elem:
    print(i.text)