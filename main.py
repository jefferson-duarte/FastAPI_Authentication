from secrets import token_hex

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import CONN, Person, Tokens

app = FastAPI()


def db_connection():
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


@app.post('/register')
def register(name: str, username: str, password: str):
    session = db_connection()
    user = session.query(Person).filter_by(
        username=username, password=password
    ).all()

    if len(user) == 0:
        register_user = Person(name=name, username=username, password=password)
        session.add(register_user)
        session.commit()
        return {'status': f'User "{name}" registed successfully.'}

    return {'status': f'User "{name}" already registed.'}


@app.post('/login')
def login(username: str, password: str):
    session = db_connection()
    user = session.query(Person).filter_by(
        username=username, password=password
    ).all()

    if len(user) == 0:
        return {'status': f'Username "{username}" does not exist.'}

    while True:
        token = token_hex(50)
        exist_token = session.query(Tokens).filter_by(token=token).all()

        if len(exist_token) == 0:
            exist_user = session.query(Tokens).filter_by(
                id_person=user[0].id
            ).all()

            if len(exist_user) == 0:
                new_token = Tokens(id_person=user[0].id, token=token)
                session.add(new_token)
            elif len(exist_user) > 0:
                exist_user[0].token = token

            session.commit()
            break

    return {'token': token}
