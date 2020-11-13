from flask import Flask
from flask import request, render_template
from form import Form
from trie import TrirTree
app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"

@app.route('/', methods=['POST', 'GET'])
def index():
    # TODO 1. concurrency 2. lower and upper 3. construct trie tree
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

@app.route('/query?item=<result>', methods=['GET'])
def show(result):
    return render_template('result.html', result=dict.search(result))

@app.route('/add?item=<location>', methods=['POST'])
def add(location):
    # db operation
    error = None
    success = None
    if dict.add(location):
        success = 'Update successfully!'
    else:
        error = "The location already exists!"
    return render_template('search.html', error=error, success=success)

@app.route('/delete?item=<location>', methods=['POST'])
def delete(location):
    # db operation
    error = None
    success = None
    if dict.delete(location):
        success = 'Delete successfully!'
    else:
        error = "The location doesn't exist!"
    return render_template('search.html', error=error, success=success)

if __name__ == '__main__':
    dict = TrirTree()
    dict.add('San Jose')
    dict.add('San Diego')
    app.run(debug=True, port=8000)