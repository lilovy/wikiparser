from src.parser.parser import Parse
from src.parser.proxy_parser import proxy_list
from src.data.db_action import (
    create_record, 
    check_exist, 
    get_definitions,
    get_words,
    )
from config import (
    url, 
    xpath, 
    content, 
    encoding, 
    file,
    )
import queue
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor


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

def check_word() -> None:
    data = load_data(file='complete.txt')
    words = load_data(file='balance.txt')
    for i in words:
        if i not in data:
            write_complete_data(i, 'wd.txt')
    # if not check_exist(word=data):
    #     write_complete_data(i, 'balance.txt')

def set_data():

    print(len(load_data()))
    print(len(set(load_data())))

def load_words():
    words = []
    for i in get_words():
        if i[0] not in words:
            write_complete_data(i[0], 'complete.txt')
            words.append(i[0])
    return words

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

        parse_wiki_page(wiki=wiki, word=word)

def parse_wiki_page(
    # parser = None,
    word: str = '',
    wiki = None,
    ):

    if not check_exist(word=word):

        if wiki is None:
            wiki = Parse(
                url, 
                xpath=xpath, 
                content=content,
                proxy=True,
                )

        wiki.request(word)
        data = wiki.parse()

        if len(data) == 0:
            if word.islower():
                wiki.request(word.capitalize())
            else:
                wiki.request(word.lower())

            data = wiki.parse()
            if len(data) == 0:
                wiki.request(word.upper())

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
        write_complete_data(word, 'complete.txt')
    else:
        # write_complete_data(word)
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
    thread_count: int = 10, 
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

# def multi_qouter(workers=4):
#     with ThreadPoolExecutor(max_workers=workers) as executor:
#         _ = [executor.submit(wi) for i in range(workers)]

def mulit_process():
    with multiprocessing.Pool(processes=100) as pool:
        pool.map(parse_wiki_page, load_data())

if __name__ == "__main__":
    parse_wiki(['жук'])
   