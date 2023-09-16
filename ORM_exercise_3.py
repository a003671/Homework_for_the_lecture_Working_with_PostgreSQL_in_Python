import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from password import password
from ORM_exercise_1 import create_tables, Publisher, Shop, Book, Stock, Sale


DNS = F'postgresql://postgres:{password}@localhost:5432/postgres'
engine = sq.create_engine(DNS)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

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

session.close()