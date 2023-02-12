from src.data.create_database import Session
from src.data.word_models import Word


def create_record(
    word: str, 
    definition: str, 
    part_of_speech: str,
    first_letter: str, 
    last_letter: str, 
    table = Word, 
    ) -> None:
    """
    Arguments:
        word: str 
        definitions: str
        first_letter: str
        last_letter: str
    """
    try:
        session = Session()
        obj = table(
            word=word, 
            definitions=definition,
            part_of_speech=part_of_speech, 
            first_letter=first_letter, 
            last_letter=last_letter,
            )

        session.add(obj)
        session.commit()
        session.close()
    except:
        with open(
            'src/data/truble.txt',
            'a+',
            encoding='windows-1251',
            ) as fl:
            fl.write(f'{word}\n')
        raise 'Error: unsupported arguments'
        
def check_exist(
    table = Word, 
    word: str = '',
    ) -> bool:
    """
    if the record exist -> return True

    else -> return False
    """
    try:
        session = Session()
        return session.query(table).filter(
            table.word == word,
            ).first() is not None
    except:
        return False

def get_definitions(
    table = Word, 
    word: str = '',
    ) -> str:
    """
    return information about the requested object
    """
    try:
        session = Session()
        data = session.query(table).filter(
            table.word == word,
            ).first()
        session.close()

        if data:
            return data
        else:
            return 'object not found'

    except:
        raise "Error..."

def del_item(
    word: str = '',
    table = Word,
    ) -> None:

    try:
        session = Session()
        session.query(table).filter(
            table.id == 1737,
            ).delete()
        session.commit()
        session.close()
    except:
        raise "Error..."

if __name__ == '_main__':
    print(del_item())