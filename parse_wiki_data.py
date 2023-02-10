from wiki_parser import Parse

url = 'https://ru.wiktionary.org/wiki/'

values = """//*[@id="mw-content-text"]/div[1]/ol[1]/li"""

pth ="""//*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/text() | 
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/a/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/a/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/span/text() |
        //*[@id="mw-content-text"]/div[1]/ol[1]/li[{n}]/span/span/span/a/span/text()"""


def load_data():
    with open('words.txt', encoding='utf-8') as fl:
        words = fl.read().split()
    return words
    ...

def main():
    words = load_data()
    wiki = Parse(url)
    wiki.xpath(values)
    wiki.content(pth)
    for word in words:
        print(wiki.parse(word))


if __name__ == "__main__":
    main()
    # print(load_data())