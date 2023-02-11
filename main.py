from src.parser.parse_wiki_data import parse_wiki, load_data

from multiprocessing.dummy import Pool

pool = Pool(3)

data = load_data()

result = pool.map(parse_wiki, data)
pool.close()
pool.join()

if __name__ == '__main__':
    # parse_wiki()
    ...