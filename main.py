from src.parser.parse_wiki_data import multi_process, save_html, load_data, check_word
from src.parser.proxy_parser import proxy_list
from src.data.db_action import get_elements
from collections import Counter


if __name__ == '__main__':
    ...
    # print(Counter(get_elements('first_letter')).most_common(8))
    # print(Counter(get_elements('last_letter')).most_common(8))
    multi_process(func=save_html, processes=61, data=load_data('wd.txt'))
    # check_word()
    # proxy_list()