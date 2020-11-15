from flask import Flask
from flask import request, jsonify
from trie import TrirTree
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from lock import RWLock
from flask_caching import Cache
from flask_classful import FlaskView, route
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
)
from datetime import timedelta
import random
app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
app.config['JWT_SECRET_KEY'] = '123456'
jwt = JWTManager(app)

class AutoCompleteSystem(FlaskView):
    def __init__(self):
        self.lock = RWLock()
        self.cache = Cache(app, config={'CACHE_TYPE': 'simple'})
        self.limiter = Limiter(
                            app,
                            key_func=get_remote_address,
                            default_limits=["2000 per day", "50 per hour"]
                        )

    @route('/query', methods=['GET'])
    def search(self):
        """ search a prefix """
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

    @route('/login', methods=['POST'])
    def login(self):
        """ login to get a access token """
        if not request.is_json:
            return jsonify({"msg": "Invalid JSON format in request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username:
            return jsonify({"msg": "Missing username"}), 400
        if not password:
            return jsonify({"msg": "Missing password"}), 400
        if username != 'admin' or password != '123456':
            return jsonify({"msg": "Invalid username or password"}), 401

        access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=2))
        return jsonify(access_token=access_token), 200

    @route('/add', methods=['POST'])
    @jwt_required
    def add(self):
        """ add a word """
        self.lock.acquire_write()
        location = request.args['location']
        error = None
        success = None
        if dict.add(location, random.randint(1, 20000)):
            success = 'Update successfully!'
        else:
            error = "The location already exists!"
        self.lock.release()
        if error:
            return jsonify({'result': error}), 400
        else:
            return jsonify({'result': success}), 200

    @route('/delete', methods=['POST'])
    @jwt_required
    def delete(self):
        """ delete a word """
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

def construct_tree(file):
    dict = TrirTree()
    f = open(file)
    line = f.readline()
    while line:
        line = line.strip('\n')
        data = line.split(' ')
        dict.add(data[1], data[0])
        line = f.readline()
    f.close()
    return dict

if __name__ == '__main__':
    dict = TrirTree()
    dict.add('San_Jose', 324)
    dict.add('San_Diego', 333323)
    dict = construct_tree('location-cnt.txt')
    AutoCompleteSystem.register(app, route_base='/')
    app.run(debug=True, port=8000)