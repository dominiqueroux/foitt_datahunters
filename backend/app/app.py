import werkzeug
from flask.scaffold import _endpoint_from_view_func
from werkzeug.utils import cached_property

import flask
from flask import request
#from flask_sqlalchemy import SQLAlchemy

import sqlalchemy
import requests
import json

flask.helpers._endpoint_from_view_func = _endpoint_from_view_func

werkzeug.cached_property = cached_property

from flask import Flask
from flask_restplus import Resource,Api

app = Flask(__name__)
api = Api(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hack_zurich:hack_zurich@postgres/hack_zurich'
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.secret_key = 'secret string'
#db = SQLAlchemy(app)

# DB_USER = 'hack_zurich'
# DB_PW = 'hack_zurich'
# DB_HOST = 'postgres'
# DB_PORT = '5432'
# DB_SCHEMA = 'hack_zurich'
# DB = 'hack_zurich'
# DRIVERNAME = "postgresql"

DB_USER = 'datahunteradmin@foittdatahuntersdb'
DB_PW = 'foitt2509_'
DB_HOST = 'foittdatahuntersdb.postgres.database.azure.com'
DB_PORT = '5432'
DB_SCHEMA = 'postgres'
DB = 'postgres'
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

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'borld'}

@api.route("/ask", methods=['GET'])
class AskToValueNet(Resource):
    def get(self):
        if 'question' in request.args:
            question = request.args['question']
        else:
            question = "What is the share of electric cars in 2016 for Wetzikon?"


        payload = {'question': question}
        headers = {'Content-Type': 'application/json', "X-API-KEY": "sjNmaCtviYzXWlS"}
        r = requests.put("https://inference.hackzurich2021.hack-with-admin.ch/api/question/hack_zurich", headers=headers, data=json.dumps(payload)) 

        if r.status_code == 200:
            resultproxy = connection.execute(r.json()["sql"])
            response = flask.jsonify([{column: value for column, value in rowproxy.items()} for rowproxy in resultproxy])
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

        else:
            print("error", r.status_code)
            response = flask.jsonify({"error" : r.status_code})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
