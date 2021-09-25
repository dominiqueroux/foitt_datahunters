import werkzeug
from flask.scaffold import _endpoint_from_view_func
from werkzeug.utils import cached_property

import flask
from flask import request

import sqlalchemy

flask.helpers._endpoint_from_view_func = _endpoint_from_view_func

werkzeug.cached_property = cached_property

from flask import Flask
from flask_restplus import Resource,Api

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'borld'}

@api.route("/ask", methods=['GET'])
class AskToValueNet(Resource):
    def get(self):
        # if 'id' in request.args:
        #     id = int(request.args['id'])
        # else:
        #     return "Error: No id field provided. Please specify an id."

        DB_USER = 'hack_zurich'
        DB_PW = 'hack_zurich'
        DB_HOST = 'postgres'
        DB_PORT = '5432'
        DB_SCHEMA = 'hack_zurich'
        DB = 'hack_zurich'
        DRIVERNAME = "postgresql"

        engine = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername=DRIVERNAME,
                username=DB_USER,
                password=DB_PW,
                host=DB_HOST,
                port=DB_PORT,
                database=DB,
            ),
            echo_pool=True,
        )
        print("connecting with engine " + str(engine))
        connection = engine.connect()

        resultproxy = connection.execute("SELECT * FROM commune_type")

        return [{column: value for column, value in rowproxy.items()} for rowproxy in resultproxy]

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
