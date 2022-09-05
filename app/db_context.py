from contextlib import contextmanager
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from settings import DB_CONNECTION

Base = declarative_base()

class EnglishWords(Base):
    __tablename__ = 'english_words'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    rus_translations = relationship('RussianWords', back_populates='eng_translation', cascade="all, delete-orphan")


class RussianWords(Base):
    __tablename__ = 'russian_words'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    eng_id = Column(Integer, ForeignKey('english_words.id'))
    eng_translation = relationship('EnglishWords', back_populates='rus_translations')



engine = create_engine(DB_CONNECTION)
Base.metadata.create_all(engine)

@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_translation(word, ln):
    word = word.lower()
    
    with get_session() as session:
        if ln =='ru':
            translations = session.query(RussianWords).filter_by(word=word).all()
            if translations:
                return [t.eng_translation.word for t in translations]

        elif ln == 'en':
            translations = session.query(EnglishWords).filter_by(word=word).first()
            if translations:
                return [t.word for t in translations.rus_translations]
    