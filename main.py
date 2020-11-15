from flask import Flask
from flask import request, jsonify
from trie import TrirTree
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from lock import RWLock
from flask_caching import Cache
from flask_classful import FlaskView, route
app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"


class AutoCompleteSystem(FlaskView):
    def __init__(self):
        self.lock = RWLock()
        self.cache = Cache(app, config={'CACHE_TYPE': 'simple'})
        self.limiter = Limiter(
                            app,
                            key_func=get_remote_address,
                            default_limits=["200 per day", "50 per hour"]
                        )

    @route('/query', methods=['GET'])
    def search(self):
        self.lock.acquire_read()
        location = request.args['item']
        data = self.cache.get(location)
        if data is not None:
            self.lock.release()
            return jsonify({'result': data}), 200
        result = dict.search(location)
        self.cache.set(location, result, timeout=100)
        self.lock.release()
        return jsonify({'result': result}), 200

    @route('/add', methods=['POST'])
    def add(self):
        self.lock.acquire_write()
        location = request.args['location']
        error = None
        success = None
        if dict.add(location):
            success = 'Update successfully!'
        else:
            error = "The location already exists!"
        self.lock.release()
        if error:
            return jsonify({'result': error}), 400
        else:
            return jsonify({'result': success}), 200

    @route('/delete', methods=['POST'])
    def delete(self):
        self.lock.acquire_write()
        location = request.args['location']
        error = None
        success = None
        if dict.delete(location):
            success = 'Delete successfully!'
        else:
            error = "The location doesn't exist!"
        self.lock.release()
        if error:
            return jsonify({'result': error}), 404
        else:
            return jsonify({'result': success}), 200

if __name__ == '__main__':
    dict = TrirTree()
    dict.add('San Jose')
    dict.add('San Diego')
    AutoCompleteSystem.register(app, route_base='/')
    app.run(debug=True, port=8000)