from src.data.db_action import create_record, check_exist
from src.parser.async_parser import Parse
from config import url, xpath, content, encoding, file
import asyncio, aiohttp


url = url
xpath = xpath
content = content
file = file


def load_data(file: str = file) -> list[str]:
    
    with open(
        f'src/data/{file}', 
        encoding=encoding,
        ) as fl:
        words = fl.read().split()
        
    return words

def write_complete_data(
    word: str,
    file: str,
    ) -> None:

    with open(
        f'src/data/{file}',
        'a+',
        encoding=encoding,
        ) as fl:
        fl.write(f'{word}\n')

def complete_data() -> list[str]:

    a = load_data(file='complete.txt')
    b = load_data()
    data = [v for v in b if v not in set(a) & set(b)]

    return data

def format_word(word: str) -> tuple[str, str]:

    word = remove_special_characters(word)
    try:
        f, l = word[0], word[-1]
    
        if word[-1] in ('ь', 'ы'):
            l = word[-2]

        return f.lower(), l.lower()
    except:
        raise "Error: empty string"

def reformat_data(data: list) -> str:

    if len(data) > 0:

        data_output = []
        for n, i in enumerate(data, start=1):
            data_output.append(f'{n}. {i}\n\n')

        data = """"""
        for i in data_output:
            data += i
    else:
        data = None

    return data

def remove_special_characters(string: str) -> str:

      result = ''

      for char in string:
        if char.isalnum() or char == '-':
          result += char

      return result
    

def parse_part_of_speech(model) -> str:

    wiki = model
    wiki.xpath(
        """
        //*[@id="mw-content-text"]/div[1]/p[2]/a[1]/text()
        """)

    try:
        part_of_speech = wiki.parse()

        part_of_speech = part_of_speech[0].split()[0]

        return remove_special_characters(part_of_speech).lower()
    except:
        return None

async def parse_wiki_page(
    parser = None,
    word: str = '',
    ):

    wiki = parser
    if not check_exist(word=word):
        if parser is None:
            wiki = Parse(url)
            wiki.xpath(xpath)
            wiki.content(content)

        await wiki.request(word)
        data = wiki.parse()

        if len(data) == 0:
            if word.islower():
                await wiki.request(word.capitalize())
                word = word.capitalize()
            else:
                await wiki.request(word.lower())
                word = word.lower()
            data = wiki.parse()

        f, l = format_word(word)
        data = reformat_data(data)
        p_of_sp = parse_part_of_speech(wiki)

        create_record(
            word=word, 
            definition=data,
            part_of_speech=p_of_sp, 
            first_letter=f, 
            last_letter=l,
            )
        write_complete_data(word)
    else:
        # write_complete_data(word)
        print(f'The word - {word.upper()} is already in the base.')


async def main():

    tasks = []
    for word in load_data():
        if not check_exist(word):
            task = asyncio.create_task(
                parse_wiki_page(
                    word=word,
                    )
                    )

            tasks.append(task)

    await asyncio.gather(*tasks)


def app():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

if __name__ == '__main__':
    app()