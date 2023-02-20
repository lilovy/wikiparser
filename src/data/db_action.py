import sqlalchemy as db
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
        word: `str` 
        definitions: `str`
        first_letter: `str`
        last_letter: `str`
    """
    try:
        with Session() as session:
            obj = table(
                word=word, 
                definitions=definition,
                part_of_speech=part_of_speech, 
                first_letter=first_letter, 
                last_letter=last_letter,
                )
            session.add(obj)
            session.commit()

    except Exception as e:
        raise e
        
def check_exist(
    table = Word, 
    word: str = '',
    ) -> bool:
    """
    if the record exist -> return True

    else -> return False
    """
    try:
        with Session() as session:
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
        with Session() as session:
            data = session.query(table).filter(
                table.word == word,
                ).first()

        if data:
            return data
        else:
            return 'object not found'

    except Exception as e:
        raise e

def get_elements(
    column = 'word',
    table = Word,
    ) -> list[str]:
    try:
        with Session() as session:
            return list(session.query(eval(f'table.{column}')))
    except Exception as e:
        raise e

def del_item(
    word: str = '',
    table = Word,
    ) -> None:

    try:
        with Session() as session:
            session.query(table).filter(
                table.word == word,
                ).delete()
            session.commit()
    except Exception as e:
        raise e
