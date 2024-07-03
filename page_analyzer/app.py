import os

import page_analyzer.html as html
import page_analyzer.urls as urls

from flask import (
    Flask,
    render_template,
    request,
    flash,
    url_for,
    redirect,
)
from dotenv import load_dotenv

from page_analyzer.db import DatabaseConnect, DatabaseUrls


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template(
        'index.html',
    )


@app.get('/urls')
def urls_get():
    data_base = DatabaseUrls(DatabaseConnect(DATABASE_URL))
    urls = data_base.get_urls()
    return render_template(
        'urls.html',
        urls=urls,
    )


@app.post('/urls')
def urls_post():
    data_base = DatabaseUrls(DatabaseConnect(DATABASE_URL))

    data = request.form.to_dict()['url']

    if not urls.is_valid_url(data):
        flash('Некорректный URL', 'error')
        return render_template(
            'index.html',
        ), 422

    url = urls.normalaize_url(data)

    if data_base.in_base(url):
        flash('Страница уже существует', 'info')
        return redirect(url_for('urls_id', id=data_base.get_id(url)))

    data_base.save(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_id', id=data_base.get_id(url)))


@app.get('/urls/<int:id>')
def urls_id(id):
    data_base = DatabaseUrls(DatabaseConnect(DATABASE_URL))

    url = data_base.find(id)
    url_checks = data_base.get_checks_data(id)
    return render_template(
        'show.html',
        id=id,
        url=url,
        url_checks=url_checks
    )


@app.post('/urls/<int:id>/checks')
def url_check(id):
    data_base = DatabaseUrls(DatabaseConnect(DATABASE_URL))

    url_name = data_base.find(id).name
    if not urls.is_valid_url(url_name):
        flash('Произошла ошибка при проверке', 'error')
        return redirect(
            url_for('urls_id', id=id)
        )

    if not urls.check_url(url_name):
        flash('Произошла ошибка при проверке', 'error')
        return redirect(
            url_for('urls_id', id=id)
        )

    url_content = html.parse_url(url_name)
    data_base.save_check_data(id, url_content, urls.get_status_code(url_name))
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_id', id=id, ))
