from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    url_for,
    redirect,
)
import os

from dotenv import load_dotenv

from page_analyzer.db import db_save, db_urls, db_get_id, db_find, db_checks, db_save_checks
from page_analyzer.functions import is_valid, normalaize_url


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')



@app.route('/')
def index():
    
    return render_template(
        'index.html'
    )


@app.route('/urls', methods = ['GET', 'POST'])
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
               ), 422
        url = normalaize_url(data)
        db_save(url)
        id = db_get_id(url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls_id', id=id))


@app.get('/urls/<int:id>')
def urls_id(id):
    url = db_find(id)
    url_name, url_created = url[0], url[1]
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
    url = db_urls()
    db_save_checks(id, url)
    # data = request.form.to_dict()['url']
    # if not is_valid(data):
    #     flash('Неккоректный URL', 'error')
    #     return render_template(
    #         'index.html'
    #         ), 422
    # url = normalaize_url(data)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_id', id=id, ))