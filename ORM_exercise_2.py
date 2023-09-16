import sqlalchemy as sq
from ORM_exercise_1 import create_tables, Publisher, Shop, Book, Stock, Sale
from password import password
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime 


DNS = F'postgresql://postgres:{password}@localhost:5432/postgres'
engine = sq.create_engine(DNS)

Session = sessionmaker(bind=engine)
session = Session()


writer = input('Input writer name or id: ')
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)

if writer.isdigit():
    query = query.filter(Publisher.id == writer).all()
else:
    query = query.filter(Publisher.name == writer).all()

for title, name, price, date_sale in query:
    print(F'{title:<40} | {name:<10} | {price:<8} | {date_sale.strftime("%m-%d-%Y, %H:%M:%S")}')

session.close()