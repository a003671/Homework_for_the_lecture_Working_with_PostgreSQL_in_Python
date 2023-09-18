import sqlalchemy as sq
from orm_exercise_1 import create_tables, Publisher, Shop, Book, Stock, Sale
from password import password
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime 


def connection_DB(login='postgres', password=password, name_server='localhost', port_server='5432', name_BD='postgres'):
    DNS = F'postgresql://{login}:{password}@{name_server}:{port_server}/{name_BD}'
    return sq.create_engine(DNS)


def find_writer(writer):
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)

    if writer.isdigit():
        query = query.filter(Publisher.id == writer).all()
    else:
        query = query.filter(Publisher.name == writer).all()

    for title, name, price, date_sale in query:
        print(F'{title:<40} | {name:<10} | {price:<8} | {date_sale.strftime("%m-%d-%Y, %H:%M:%S")}')


if __name__ == '__main__':
    login = input('enter your database login: ')
    password = input('enter your database password: ')
    name_server = input('enter your name server: ')
    port_server = input('enter your database port server: ')
    name_BD = input('enter your database name: ')
    engine = connection_DB()
    Session = sessionmaker(bind=engine)
    session = Session()
    find_writer(input('Input writer name or id: '))
    session.close()