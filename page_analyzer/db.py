import os
import psycopg2

from psycopg2.extras import NamedTupleCursor
from datetime import date

DATABASE_URL = os.getenv('DATABASE_URL')

def db_save(data):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO urls (name, created_at) VALUES \
                       (%s, %s)', (data, date.today()))
    conn.commit() 
    conn.close()



def db_find(id):
    item = ()
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as curs:
        curs.execute('SELECT name, created_at FROM urls WHERE id=%s', (int(id),))
        item = curs.fetchone()
    conn.close()
    return item


def db_urls():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT urls.id,\
                    urls.name,\
                    url_checks.created_at,\
                    url_checks.status_code\
                    FROM urls INNER JOIN url_checks ON\
                        urls.id = url_checks.url_id\
                    ORDER BY id DESC')
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


def db_checks(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT id, status_code, h1,\
                      title, description, created_at \
                     FROM url_checks WHERE url_id=%s ORDER BY id DESC', (id,))
        url_checks = curs.fetchall()
    conn.close()
    return url_checks


def db_save_checks(id, data):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO url_checks (url_id, created_at) VALUES \
                       (%s, %s)', (id, date.today()))
    conn.commit() 
    conn.close()