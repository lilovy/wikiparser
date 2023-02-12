from src.parser.parser import Parse
from src.data.db_action import create_record, check_exist, get_definitions
from config import url, xpath, content, encoding
import queue
import threading

url = url
xpath = xpath
content = content


def load_data() -> list[str]:
    
    with open(
        'src/data/nouns.txt', 
        encoding=encoding,
        ) as fl:
        words = fl.read().split()
        
    return words

def format_word(word: str) -> tuple[str, str]:

    word = remove_special_characters(word)
    try:
        f, l = word[0], word[-1]
    
        if word[-1] in ('ь'):
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

def prs(
    word: str, 
    definition: str, 
    part_of_speech: str,
    first_letter: str, 
    last_letter: str,
    ) -> None:

    create_record(
        word=word, 
        definition=definition, 
        part_of_speech=part_of_speech,
        first_letter=first_letter, 
        last_letter=last_letter,
        )

def remove_special_characters(string: str) -> str:
    # return ''.join(e  for e in string else e == '-' if e.isalnum())
      # Create an empty string
      result = ''
      # Iterate over the characters of the string
      for char in string:
        # Only add non-special characters to the result string
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

def parse_wiki(
    words: list = load_data(),
    ):

    wiki = Parse(url)
    # wiki.xpath(xpath)
    # wiki.content(content)

    for n, word in enumerate(words, start=1):
        wiki.xpath(xpath)
        wiki.content(content)
        print(word)
        print(f"""parse {n} word of {len(words)} -> {round(n/len(words)*100, 1)}% processed""")

        parse_wiki_page(parser=wiki, word=word)

def parse_wiki_page(
    parser = None,
    word: str = '',
    ):

    wiki = parser

    if not check_exist(word=word):

        if parser is None:
            wiki = Parse(url)
            wiki.xpath(xpath)
            wiki.content(content)

        wiki.request(word)
        data = wiki.parse()
        if len(data) == 0:
            if word.islower():
                wiki.request(word.capitalize())
            else:
                wiki.request(word.lower())
            data = wiki.parse()

        f, l = format_word(word)
        data = reformat_data(data)
        p_of_sp = parse_part_of_speech(wiki)
        # print(data)
        # print(p_of_sp)

        prs(
            word=word, 
            definition=data,
            part_of_speech=p_of_sp, 
            first_letter=f, 
            last_letter=l,
            )
    else:
        print(f'The word - {word.upper()} is already in the base.')

def worker(url_queue) -> None:

    queue_full = True
    
    while queue_full:
        try:
            # Get your data off the queue, and do some work
            word = url_queue.get(False)
            parse_wiki_page(word=word)
            # print(len(data))

        except queue.Empty:
            queue_full = False

def multiprocessing_parse(
    thread_count: int = 15, 
    data: list = load_data(),
    ) -> None:

    q = queue.Queue()
    # data = load_data()

    for d in data:
        q.put(d)

    # Create as many threads as you want
    for i in range(thread_count):
        t = threading.Thread(target=worker, args = (q,))
        t.start()


if __name__ == "__main__":
    parse_wiki(['жук'])
   