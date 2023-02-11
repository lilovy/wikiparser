from src.parser.parser import Parse
from src.data.db_action import create_record, check_exist
from config import url, xpath, content

url = url
xpath = xpath
content = content


def load_data() -> list[str]:
    
    with open(
        'src/data/words.txt', 
        encoding='utf-8',
        ) as fl:
        words = fl.read().split()
        
    return words

def format_word(word: str) -> tuple[str, str]:

    f, l = word[0], word[-1]

    if word[-1] == 'ь':
        l = word[-2]
        
    return f, l

def reformat_data(data: list) -> str:

    data_output = []

    for n, i in enumerate(data, start=1):
        data_output.append(f'{n}. {i}\n\n')

    data = """"""
    for i in data_output:
        data += i
        
    return data

def prs(
    word: str, 
    definition: str, 
    first_letter: str, 
    last_letter: str,
    ) -> None:

    create_record(
        word=word, 
        definition=definition, 
        first_letter=first_letter, 
        last_letter=last_letter,
        )

def main(
    words: list = load_data(),
    ):

    wiki = Parse(url)
    wiki.xpath(xpath)
    wiki.content(content)

    for n, word in enumerate(words, start=1):
        print(f'parse {n} word of {len(words)} -> {round(n/len(words)*100, 1)}% processed')
        if not check_exist(word=word):

            f, l = format_word(word)
            data = wiki.parse(word)
            data = reformat_data(data)
            
            prs(
                word=word, 
                definition=data, 
                first_letter=f, 
                last_letter=l,
                )
        else:
            print(f'The word - {word} is already in the base.')


if __name__ == "__main__":
    main()
    # print(get_definitions(word="конь"))
    # print(load_data())