from src.data.create_database import Session
from src.data.word_models import Word


def create_record(
    word: str, 
    definition: str, 
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
            first_letter=first_letter, 
            last_letter=last_letter,
            )

        session.add(obj)
        session.commit()
        session.close()
    except:
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
        raise 'Error'

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

if __name__ == '_main__':
    print(get_definitions(word='конь'))