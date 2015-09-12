import os
import random
import string
import datetime

from flask import Flask, request, redirect, render_template, flash
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import TextField
from wtforms.validators import Required

from config import config


basedir = os.path.abspath(os.path.dirname(__file__))

# Config
DEBUG = config['debug']
SECRET_KEY = config['key']
USERNAME = config['username']
PASSWORD = config['password']

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, config['db'])

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

# globals
address = config['address']  # This is our address


# Form
class UrlForm(Form):
    url = TextField('URL', [Required()])


# Model
class MiniURL(db.Model):
    __tablename__ = 'miniurl'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    hash = db.Column(db.String(10), unique=True)
    url = db.Column(db.String(120))

    def __init__(self, hash=None, url=None):
        self.hash = hash
        self.url = url

    def __repr__(self):
        return '<MiniUrl %r:%r>' % (self.hash, self.url)


# Helper functions
def get_hashes():
    hashes = [x.hash for x in MiniURL.query.all()]
    return hashes


def get_recent(amount):
    hashes = get_hashes()
    return hashes[:-(amount + 1):-1]


def url_check(url):
    '''Attempt to ensure a valid url'''
    if len(url.split('://')) != 2:
        url = 'http://' + url
    return url


def build_rand(size):
    '''Generate a random string 62**size'''
    base = string.digits + string.letters
    hashes = get_hashes()
    while True:
        rand = ''.join([random.choice(base) for x in xrange(size)])
        if rand not in hashes:
            break
    return rand


# Controllers
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm(request.form)
    if form.validate_on_submit():
        new_hash = build_rand(5)
        new_url = MiniURL(hash=new_hash, url=url_check(form.url.data))
        try:
            db.session.add(new_url)
            db.session.commit()
        except:
            flash('There was a problem with your request. It\'s not you,'
                  ' it\'s us.')
        return render_template('index.html',
                               result=address + '/' + new_hash,
                               links=get_recent(10),
                               home=address,
                               form=form)
    return render_template('index.html',
                           links=get_recent(10),
                           home=address,
                           form=form)


@app.route('/<lookup>')
def lookup(lookup):
    try:
        url = MiniURL.query.filter_by(hash=lookup).first()
        return redirect(url.url, code=302)
    except:
        form = UrlForm(request.form)
        return render_template('index.html',
                               links=get_recent(10),
                               home=address,
                               form=form)


if __name__ == '__main__':
    app.run()
