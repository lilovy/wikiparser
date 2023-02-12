from sqlalchemy import Column, Integer, String, Text
from src.data.create_database import Base, create_db


class Word(Base):
    __tablename__ = 'word_dictionary'

    id = Column(Integer, primary_key=True)
    word = Column(String(50))
    definitions = Column(Text(), default=None)
    part_of_speech = Column(String(25), default=None)
    first_letter = Column(String(10))
    last_letter = Column(String(10))

    def __init__(
        self, word: str, 
        definitions: str, 
        part_of_speech: str, 
        first_letter: str, 
        last_letter: str,
        ):

        self.word = word
        self.definitions = definitions
        self.part_of_speech = part_of_speech
        self.first_letter = first_letter
        self.last_letter = last_letter

    def __repr__(self):
        info: str = f'{self.word} - {self.part_of_speech}: \n\n' \
                    f'{self.definitions}\n'
        return info


create_db()
