from src.parser.parse_wiki_data import load_data

file = 'src/data/de.txt'

with open(
    file, 
    'a',
    encoding='utf-8', 
    ) as f:
    for i in load_data():
        f.write(f'{i}\n')

        