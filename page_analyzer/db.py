import psycopg2

from psycopg2.extras import NamedTupleCursor
from datetime import date


class DatabaseConnect:
    def __init__(self, db_url):
        self.db_url = db_url

    def __enter__(self):
        self.conn = psycopg2.connect(self.db_url)
        return self.conn.cursor(cursor_factory=NamedTupleCursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class DatabaseUrls:
    def __init__(self, db_connect):
        self.db_connect = db_connect

    def save(self, data):
        with self.db_connect as cursor:
            cursor.execute('INSERT INTO urls (name, created_at) VALUES \
                       (%s, %s)', (data, date.today()))

    def find(self, id):
        item = ()
        with self.db_connect as cursor:
            cursor.execute('SELECT name, created_at \
                            FROM urls WHERE id=%s', (int(id),))
            item = cursor.fetchone()
        return item

    def get_urls(self):
        with self.db_connect as cursor:
            cursor.execute('SELECT DISTINCT ON (urls.id) urls.id,\
                        urls.name,\
                        url_checks.created_at,\
                        url_checks.status_code\
                        FROM urls LEFT JOIN url_checks ON\
                            urls.id = url_checks.url_id\
                        ORDER BY id DESC')
            data = cursor.fetchall()
        return data

    def get_id(self, url):
        with self.db_connect as cursor:
            cursor.execute('SELECT id FROM urls WHERE name=%s', (url,))
            id = cursor.fetchone()
        return id.id

    def get_checks_data(self, id):
        with self.db_connect as cursor:
            cursor.execute('SELECT id, status_code, h1,\
                        title, description, created_at \
                        FROM url_checks WHERE url_id=%s \
                        ORDER BY id DESC', (id,))
            cheks_data = cursor.fetchall()
        return cheks_data

    def save_check_data(self, id, url_content, status_code):
        h1 = url_content.get("h1", "")
        title = url_content.get("title", "")
        description = url_content.get("description", "")
        with self.db_connect as cursor:
            cursor.execute(
                "INSERT INTO url_checks \
            (url_id, status_code, h1,\
            title, description, created_at) VALUES \
            (%s, %s, %s, %s, %s, %s)",
                (id, status_code, h1, title, description, date.today()),
            )

    def in_base(self, data):
        with self.db_connect as cursor:
            cursor.execute('SELECT * FROM urls WHERE name=%s', (data,))
            result = cursor.fetchall()
        if not result:
            return False
        return True
