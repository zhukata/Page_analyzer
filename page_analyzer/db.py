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
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute('SELECT name, created_at \
                       FROM urls WHERE id=%s', (int(id),))
        item = cursor.fetchone()
    conn.close()
    return item


def db_urls():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute('SELECT DISTINCT ON (urls.id) urls.id,\
                    urls.name,\
                    url_checks.created_at,\
                    url_checks.status_code\
                    FROM urls LEFT JOIN url_checks ON\
                        urls.id = url_checks.url_id\
                    ORDER BY id DESC')
        data = cursor.fetchall()
    conn.close()
    return data


def db_get_id(data):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM urls WHERE name=%s', (data,))
        id = cursor.fetchone()[0]
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


def db_save_checks(id, url_content, status_code):
    h1 = url_content.get('h1', '')
    title = url_content.get('title', '')
    description = url_content.get('description', '')
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO url_checks \
                       (url_id, status_code, h1,\
                        title, description, created_at) VALUES \
                       (%s, %s, %s, %s, %s, %s)',
                       (id, status_code, h1, title, description, date.today()))
    conn.commit()
    conn.close()


def in_base(data):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM urls WHERE name=%s', (data,))
        result = cursor.fetchall()
    conn.close()
    if not result:
        return False
    return True
