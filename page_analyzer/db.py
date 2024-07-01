import os
import psycopg2

from datetime import date

DATABASE_URL = os.getenv('DATABASE_URL')

def db_save(data):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO urls(name, created_at) VALUES (%s, %s)', (data, date.today()))
    conn.commit() 
    conn.close()



def db_find(id):
    item = ()
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as curs:
        curs.execute('SELECT name, created_at FROM urls WHERE id=%s', (id,))
        item = curs.fetchone()
    conn.close()
    return item


def db_urls():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls ORDER BY id DESC')
        data = curs.fetchall()
    conn.close()
    return data


def db_get_id(data):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as curs:
        curs.execute('SELECT id FROM urls WHERE name=%s', (data,))
        id = curs.fetchone()[0]
    conn.close()
    return id
