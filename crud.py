import psycopg2
from password import password

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
                    DROP TABLE phone;
                    DROP TABLE info;
                    '''); 
              
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS info(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    surname VARCHAR(60) NOT NULL,  
                    email VARCHAR(100) NOT NULL UNIQUE);
                    ''')
        conn.commit()

        cur.execute(''' 
                    CREATE TABLE IF NOT EXISTS phone(
                    id SERIAL PRIMARY KEY,
                    number VARCHAR(15) UNIQUE NULL,
                    id_info int NULL REFERENCES info(id));
                    ''')
        conn.commit()


def add_client(conn, name, surname, email, number=None):
    with conn.cursor() as cur:
        cur.execute('''
                    INSERT INTO info(name, surname, email) 
                    VALUES(%s, %s, %s);
                    ''', (name, surname, email))
        conn.commit()

        cur.execute('''
                    SELECT id FROM info
                    WHERE name=%s and surname=%s and email=%s
                    ''', (name, surname, email))
        
        id = cur.fetchone()
        if number: add_phone(conn, id, number)


def add_phone(conn, id, number):
    with conn.cursor() as cur:
        cur.execute('''
                    INSERT INTO phone(number, id_info)
                    VALUES(%s, %s);
                    ''', (number, id))
        conn.commit()


def change_client(conn, id, name=None, surname=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute('''
                    UPDATE info
                    SET name=%s, surname=%s, email=%s
                    WHERE id=%s
                    RETURNING id, name, surname, email;
                    ''', (name, surname, email, id))
        conn.commit()

        if number: add_phone(conn, id, number)
        

def delete_phone(conn, number):
    with conn.cursor() as cur:
        cur.execute('''
                    DELETE FROM phone
                    WHERE number=%s
                    ''', (number,))
        conn.commit()


def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute('''
                    SELECT number FROM phone
                    WHERE id_info=%s
                    ''', (id,))
        number = cur.fetchone()
        delete_phone(conn, number)
        
        cur.execute('''
                    DELETE FROM info
                    WHERE id=%s
                    ''', (id,))
        conn.commit()


def find_client(conn, name=None, surname=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute('''
                    SELECT id, name, surname, email FROM info
                    WHERE name=%s or surname=%s or email=%s
                    ''', (name, surname, email))
        find_info = cur.fetchall()
        for id, name, surname, email in find_info:
            cur.execute('''
                    SELECT number FROM phone
                    WHERE id_info=%s
                    ''', (id,))
            number = cur.fetchall()
            print(name, surname, email, *number)

        
with psycopg2.connect(database='clients_db', user='postgres', password=password) as conn:
    create_db(conn)
    add_client(conn, 'Семен', 'Семенов', 'SemenSemenov@mail.ru', 89654987654)
    add_client(conn, 'Иван', 'Иванов', 'IvanIvanof@mail.ru')
    add_phone(conn, 2, 89564213598)
    change_client(conn, 2, 'Ivan', 'Ivanov', 'IvanIvanov@rambler.com', 25987145698)
    add_client(conn, 'Ivan', 'Semenov', 'SemenovIvan@yandex.ru', 25874125963)

    add_phone(conn, 1, 85123695472)
    delete_phone(conn, '89654987654')
    add_client(conn, 'Сергей', 'Иванов', 'SergeyIvanov@yandex.ru', 85123654782)
    delete_client(conn, 3)   
    add_client(conn, 'Ivan', 'Semenov', 'SemenovIvan@yandex.ru', 25874125698)
    find_client(conn, surname='Semenov')
    find_client(conn, email='IvanIvanov@rambler.com')
    find_client(conn, name='Ivan')

conn.close()