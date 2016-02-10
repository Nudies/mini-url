import os
import json
import string
import random
import datetime

from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, render_template, flash, session, url_for
from wtforms import TextField
from wtforms.validators import Required


# globals
ADDRESS = 'localhost:5000'


# Config
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='this-needs-to-be-changed',
    USERNAME='admin',
    PASSWORD='default',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy(app)


# Forms
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
        self.timestamp = datetime.datetime.utcnow()

    def __repr__(self):
        return '<MiniUrl %r:%r>' % (self.hash, self.url)


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    platform = db.Column(db.String(120))
    browser = db.Column(db.String(120))
    version = db.Column(db.String(60))
    language = db.Column(db.String(120))
    ua_string = db.Column(db.String(256))
    ip = db.Column(db.String(256))

    def __init__(self, plat, browser, ver, lang, ua, ip):
        self.platform = plat
        self.browser = browser
        self.version = ver
        self.language = lang
        self.ua_string = ua
        self.ip = ip
        self.timestamp = datetime.datetime.utcnow()


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


def get_browsers(query):
    browsers = {}
    for entry in query:
        browser = getattr(entry, 'browser')
        if not browsers.get(browser, False):
            browsers[browser] = 1
        else:
            browsers[browser] += 1
    return browsers


def get_platforms(query):
    platforms = {}
    for entry in query:
        platform = getattr(entry, 'platform')
        if not platforms.get(platform, False):
            platforms[platform] = 1
        else:
            platforms[platform] += 1
    return platforms


def get_months(query):
    months = {}
    for entry in query:
        month = getattr(entry, 'timestamp')
        month = month.strftime('%b')
        if not months.get(month, False):
            months[month] = 1
        else:
            months[month] += 1
    return months


# Controllers
@app.before_request
def unique_visits():
    if session.get('unique_visit', False):
        return
    session['unique_visit'] = True
    ua = request.user_agent
    stats = Stats(
        ua.platform,
        ua.browser,
        ua.version,
        ua.language,
        ua.string,
        request.remote_addr
    )
    db.session.add(stats)
    db.session.commit()


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
        return render_template(
            'index.html',
            result=ADDRESS + '/' + new_hash,
            links=get_recent(10),
            home=ADDRESS,
            form=form
        )
    return render_template(
        'index.html',
        links=get_recent(10),
        home=ADDRESS,
        form=form
    )


@app.route('/stats')
def stats():
    return render_template('stats.html')


@app.route('/data/<param>')
def data(param):
    stats = Stats.query.all()
    if param == 'browsers':
        browsers = get_browsers(stats)
        return json.dumps(browsers)
    elif param == 'platforms':
        platforms = get_platforms(stats)
        return json.dumps(platforms)
    elif param == 'months':
        months = get_months(stats)
        return json.dumps(months)
    else:
        return redirect(url_for('index'))


@app.route('/<lookup>')
def lookup(lookup):
    try:
        url = MiniURL.query.filter_by(hash=lookup).first()
        return redirect(url.url, code=302)
    except:
        return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run()
