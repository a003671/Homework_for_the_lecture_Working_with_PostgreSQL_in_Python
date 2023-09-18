import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from password import password
from orm_exercise_1 import create_tables, Publisher, Shop, Book, Stock, Sale


def connection_DB(login='postgres', password=password, name_server='localhost', port_server='5432', name_BD='postgres'):
    DNS = F'postgresql://{login}:{password}@{name_server}:{port_server}/{name_BD}'
    return sq.create_engine(DNS)


def filling_tables():
    with open('test.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


if __name__ == '__main__':
    login = input('enter your database login: ')
    password = input('enter your database password: ')
    name_server = input('enter your name server: ')
    port_server = input('enter your database port server: ')
    name_BD = input('enter your database name: ')
    engine = connection_DB()
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    filling_tables()
    session.close()