import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CONN = 'sqlite:///sqlite.db'

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(15))


class Tokens(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    id_person = Column(Integer, ForeignKey('person.id'))
    token = Column(String(100))
    data = Column(DateTime, default=datetime.datetime.now())


Base.metadata.create_all(engine)
