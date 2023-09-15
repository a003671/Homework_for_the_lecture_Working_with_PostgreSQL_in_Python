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


def add_client(conn, name, surname, email, number=None):
    with conn.cursor() as cur:
        cur.execute('''
                    INSERT INTO info(name, surname, email) 
                    VALUES(%s, %s, %s);
                    ''', (name, surname, email))
        

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
        

def change_client(conn, id, name=None, surname=None, email=None, number=None):
    with conn.cursor() as cur:
        if name:
            cur.execute('''
                    UPDATE info
                    SET name=%s
                    WHERE id=%s
                    ''', (name, id))
        if surname:
            cur.execute('''
                    UPDATE info
                    SET surname=%s
                    WHERE id=%s
                    ''', (surname, id))
        if email:
            cur.execute('''
                    UPDATE info
                    SET email=%s
                    WHERE id=%s
                    ''', (email, id))
        
        if number: add_phone(conn, id, number)
        

def delete_phone(conn, number):
    with conn.cursor() as cur:
        cur.execute('''
                    DELETE FROM phone
                    WHERE number=%s
                    ''', (number,))


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
   

def find_client(conn, name=None, surname=None, email=None, number=None):
    with conn.cursor() as cur:
        if name:
            cur.execute('''
                    SELECT i.id, i.name, i.surname, i.email, p.number
                    FROM info as i
                    LEFT JOIN phone AS p on i.id = p.id_info
                    WHERE name=%s
                    ''', (name,))

        if surname:
            cur.execute('''
                    SELECT i.id, i.name, i.surname, i.email, p.number
                    FROM info as i
                    LEFT JOIN phone AS p on i.id = p.id_info
                    WHERE surname=%s
                    ''', (surname,))
        if email:
            cur.execute('''
                    SELECT i.id, i.name, i.surname, i.email, p.number
                    FROM info as i
                    LEFT JOIN phone AS p on i.id = p.id_info
                    WHERE email=%s
                    ''', (email,))
        if number:
            cur.execute('''
                    SELECT p.number, i.id, i.name, i.surname, i.email
                    FROM phone as p
                    LEFT JOIN info AS i on p.id_info = i.id
                    WHERE number=%s
                    ''', (number,))
        
        print(cur.fetchall())
        



if __name__ == '__main__':   
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
        change_client(conn, 2, name='Sergey')
        change_client(conn, 1, email='SergeyIvanov@rambler.ru')
        change_client(conn, 2, name='Сергей')
        find_client(conn, surname='Semenov')
        find_client(conn, email='SergeyIvanov@yandex.ru')
        find_client(conn, name='Сергей')
        find_client(conn, name='Сергей', surname='Ivanov')
        find_client(conn, number='25874125698')


    conn.close()