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

from page_analyzer.db import db_save, db_urls, db_get_id, db_find
from page_analyzer.db import db_checks, db_save_checks, in_base
import page_analyzer.html as html
import page_analyzer.urls as urls


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template(
        'index.html',
    )


@app.get('/urls')
def urls_get():
    urls = db_urls()
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
    id = db_get_id(url)

    if in_base(url):
        flash('Страница уже существует', 'info')
        return redirect(url_for('urls_id', id=id))

    db_save(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_id', id=id))


@app.get('/urls/<int:id>')
def urls_id(id):
    url = db_find(id)
    url_checks = db_checks(id)
    return render_template(
        'show.html',
        id=id,
        url=url,
        url_checks=url_checks
    )


@app.post('/urls/<int:id>/checks')
def url_check(id):
    url = db_find(id).name
    if not urls.is_valid_url(url):
        flash('Произошла ошибка при проверке', 'error')
        return redirect(
            url_for('urls_id', id=id)
        )

    url_content = html.parse_url(url)
    db_save_checks(id, url_content, urls.check_url(url))
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_id', id=id, ))
