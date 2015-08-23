import random
import string

from flask import Flask, request, redirect, render_template

# Config
DEBUG = True
SECRET_KEY = 'this-needs-to-be-changed'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

# globals
address = 'http://localhost:5000'  # This is our address
db = {}  # Replace this with a real database


# Helper functions
def url_check(url):
    '''Attempt to ensure a valid url'''
    if len(url.split('://')) != 2:
        url = 'http://' + url
    return url


def build_rand(size):
    '''Generate a random string 62**size'''
    global db
    base = string.digits + string.letters
    while True:
        rand = ''.join([random.choice(base) for x in xrange(size)])
        if rand not in db.keys():
            break
    return rand


# Controllers
@app.route('/', methods=['GET', 'POST'])
def index():
    global db
    if request.method == 'POST':
        form = request.form['url']
        hash = build_rand(5)
        db[hash] = url_check(form)
        return render_template('index.html', 
                               result='http://localhost:5000/%s' % hash, 
                               links=db.keys(),
                               home=address)
    return render_template('index.html',
                           links=db.keys(),
                           home=address)


@app.route('/<hash>')
def lookup(hash):
    global db
    try:
        url = db[hash]
        return redirect(url, code=302)
    except KeyError:
        return render_template('index.html',
                               links=db.keys(),
                               home=address)

if __name__ == '__main__':
    app.run()
