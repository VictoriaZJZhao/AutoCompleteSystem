from flask import Flask
from flask import request, render_template
from form import Form
from trie import TrirTree
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from lock import RWLock
app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/', methods=['POST', 'GET'])
def index():
    # TODO 1. lower and upper 2. construct trie tree
    form = Form()
    if request.method == 'POST':
        word = request.form['word']
        if form.search.data:
            return show(word)
        if form.add.data:
            return add(word)
        if form.delete.data:
            return delete(word)
    return render_template('search.html', error=None, success=None)

@app.route('/query?item=<locations>', methods=['GET'])
def show(locations):
    lock.acquire_read()
    result = dict.search(locations)
    if len(result) == 0:
        lock.release()
        return render_template('search.html', error=None, success="Nothing")
    lock.release()
    return render_template('search.html', error=None, success=result)

@app.route('/add?item=<location>', methods=['POST'])
def add(location):
    lock.acquire_write()
    error = None
    success = None
    if dict.add(location):
        success = 'Update successfully!'
    else:
        error = "The location already exists!"
    lock.release()
    return render_template('search.html', error=error, success=success)

@app.route('/delete?item=<location>', methods=['POST'])
def delete(location):
    lock.acquire_write()
    error = None
    success = None
    if dict.delete(location):
        success = 'Delete successfully!'
    else:
        error = "The location doesn't exist!"
    lock.release()
    return render_template('search.html', error=error, success=success)

if __name__ == '__main__':
    dict = TrirTree()
    lock = RWLock()
    dict.add('San Jose')
    dict.add('San Diego')
    app.run(debug=True, port=8000)