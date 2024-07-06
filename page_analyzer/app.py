import os

from flask import (
    Flask,
    render_template,
    request,
    flash,
    url_for,
    redirect,
)
from dotenv import load_dotenv

import page_analyzer.db as db
import page_analyzer.html as html
import page_analyzer.urls as urls


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')

DatabaseURL = db.UrlRepository(db.DatabaseConnection(DATABASE_URL))


@app.route('/')
def index():
    return render_template(
        'index.html',
    )


@app.get('/urls')
def urls_get():
    urls = DatabaseURL.get_urls()

    return render_template(
        'urls.html',
        urls=urls,
    )


@app.post('/urls')
def urls_post():
    data = request.form.to_dict()['url']

    if not urls.is_valid_url(data):
        flash('Некорректный URL', 'error')
        return render_template(
            'index.html',
        ), 422

    url = urls.normalaize_url(data)
    if DatabaseURL.is_exists(url):
        flash('Страница уже существует', 'info')
    else:
        DatabaseURL.save(url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_id', id=DatabaseURL.get_id(url)))


@app.get('/urls/<int:id>')
def urls_id(id):
    url = DatabaseURL.get(id)
    url_checks = DatabaseURL.get_url_checks(id)

    return render_template(
        'show.html',
        id=id,
        url=url,
        url_checks=url_checks
    )


@app.post('/urls/<int:id>/checks')
def url_check(id):
    url_name = DatabaseURL.get(id).name

    status_code = urls.check_url(url_name)
    if not status_code:
        flash('Произошла ошибка при проверке', 'error')
    else:
        url_content = html.get_url_content(html.parse_url(url_name))
        DatabaseURL.save_check(id, url_content, status_code)
        flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_id', id=id, ))
