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
import psycopg2
import validators

from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

@app.route('/')
def hello():
    return render_template(
        'index.html'
    )


@app.route('/urls', methods = ['GET', 'POST'])
def urls():

    if request.method == 'GET':
        return render_template(
            'show.html'
        )
    
    if request.method == 'POST':
        data = request.form.to_dict()
        if not validators.url.url(data):
            return render_template(
                'index.html',
               ), 422

        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('posts_get'))

@app.get('/urls/<int:id>')
def urls_id(id):
    return render_template(
        'new.html'
    )