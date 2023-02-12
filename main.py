from src.parser.parse_wiki_data import multiprocessing_parse, parse_wiki, parse_wiki_page, remove_special_characters
from src.data.db_action import del_item

if __name__ == '__main__':
    # parse_wiki_page('жук')
    # parse_wiki()
    multiprocessing_parse()
    # del_item()
    # parse_wiki_page(word='аввакум')

