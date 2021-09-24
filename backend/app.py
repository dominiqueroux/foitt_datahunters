import werkzeug
from flask.scaffold import _endpoint_from_view_func
from werkzeug.utils import cached_property

import flask

flask.helpers._endpoint_from_view_func = _endpoint_from_view_func

werkzeug.cached_property = cached_property

from flask import Flask
from flask_restplus import Resource,Api

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True)
