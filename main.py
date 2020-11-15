from flask import Flask
from flask import request, render_template, redirect, url_for, jsonify
from trie import TrirTree
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from lock import RWLock
from flask_caching import Cache
app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/query', methods=['GET'])
def show():
    lock.acquire_read()
    location = request.args['item']
    data = cache.get(location)
    if data is not None:
        lock.release()
        return jsonify({'result': data}), 200
    result = dict.search(location)
    cache.set(location, result, timeout=100)
    lock.release()
    return jsonify({'result': result}), 200

@app.route('/add', methods=['POST'])
def add():
    lock.acquire_write()
    location = request.args['location']
    error = None
    success = None
    if dict.add(location):
        success = 'Update successfully!'
    else:
        error = "The location already exists!"
    lock.release()
    if error:
        return jsonify({'result': error}), 400
    else:
        return jsonify({'result': success}), 200

@app.route('/delete', methods=['POST'])
def delete():
    lock.acquire_write()
    location = request.args['location']
    error = None
    success = None
    if dict.delete(location):
        success = 'Delete successfully!'
    else:
        error = "The location doesn't exist!"
    lock.release()
    if error:
        return jsonify({'result': error}), 404
    else:
        return jsonify({'result': success}), 200

if __name__ == '__main__':
    dict = TrirTree()
    lock = RWLock()
    dict.add('San Jose')
    dict.add('San Diego')
    app.run(debug=True, port=8000)