from flask import (
    Flask,
    render_template,
    request,
    flash,
    url_for,
    redirect,
)
import os

from dotenv import load_dotenv

from page_analyzer.db import db_save, db_urls, db_get_id, db_find
from page_analyzer.db import db_checks, db_save_checks, in_base
from page_analyzer.functions import is_valid, normalaize_url
from page_analyzer.functions import check_url, parse_url


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template(
        'index.html'
    )


@app.route('/urls', methods=['GET', 'POST'])
def urls():

    if request.method == 'GET':
        urls = db_urls()
        return render_template(
            'urls.html',
            urls=urls
        )
    if request.method == 'POST':
        data = request.form.to_dict()['url']

        if not is_valid(data):
            flash('Неккоректный URL', 'error')
            return render_template(
                'index.html'
            )
        url = normalaize_url(data)

        if in_base(url):
            flash('Страница уже существует', 'info')
            return render_template(
                'index.html'
            )
        db_save(url)
        id = db_get_id(url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls_id', id=id))


@app.get('/urls/<int:id>')
def urls_id(id):
    url = db_find(id)
    url_name, url_created = url.name, url.created_at
    url_checks = db_checks(id)

    return render_template(
        'show.html',
        id=id,
        url_name=url_name,
        url_created=url_created,
        url_checks=url_checks
    )


@app.post('/urls/<int:id>/checks')
def url_check(id):
    url = db_find(id).name
    if not check_url(url):
        flash('Произошла ошибка при проверке', 'error')
        return redirect(
            url_for('urls_id', id=id)
        )

    url_content = parse_url(url)
    db_save_checks(id, url_content, check_url(url))
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_id', id=id, ))
