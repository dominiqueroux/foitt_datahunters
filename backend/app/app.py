import werkzeug
from flask.scaffold import _endpoint_from_view_func
from werkzeug.utils import cached_property

import flask
from flask import request

flask.helpers._endpoint_from_view_func = _endpoint_from_view_func

werkzeug.cached_property = cached_property

from flask import Flask
from flask_restplus import Resource,Api

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'rorld'}

@api.route("/ask", methods=['GET'])
class AskToValueNet(Resource):
    def get(self):
        if 'id' in request.args:
            id = int(request.args['id'])
        else:
            return "Error: No id field provided. Please specify an id."

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
