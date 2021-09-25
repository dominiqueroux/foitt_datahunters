import werkzeug
from flask.scaffold import _endpoint_from_view_func
from werkzeug.utils import cached_property

import flask
from flask import request
#from flask_sqlalchemy import SQLAlchemy

import sqlalchemy
import requests
import json
import re

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

         # Get SQL query
        payload = {'question': question}
        headers = {'Content-Type': 'application/json', "X-API-KEY": "sjNmaCtviYzXWlS"}
        r = requests.put("https://inference.hackzurich2021.hack-with-admin.ch/api/question/hack_zurich", headers=headers, data=json.dumps(payload)) 

        if r.status_code == 200:
            response = {}

            # Get the «standard» data
            sql_statement = r.json()["sql"]
            resultproxy = connection.execute(sql_statement)
            standard_data = [{column: value for column, value in rowproxy.items()} for rowproxy in resultproxy]
            response["standard_data"] = standard_data

            # Calculate extended query
            #sql_statement = "SELECT T1.share_electric_cars FROM share_electric_cars AS T1 JOIN spatialunit AS T2 ON T1.spatialunit_id = T2.spatialunit_id WHERE T1.year = 2016 and T2.name = 'Wetzikon'       "
            m = re.search('(SELECT )([a-zA-Z1-9._]+)( FROM )', sql_statement)
            select_column = m.group(2)
            splitted_query = [string.split("FROM") for string in sql_statement.split("WHERE")]
            middle_query = splitted_query[0][1]
            where_clause = splitted_query[1][0].split(" and ")[1]
            year_column = splitted_query[1][0].split(" and ")[0].split(" = ")[0]
            new_query = "SELECT AVG("+select_column+"), "+year_column+" FROM "+middle_query+" WHERE "+where_clause+" GROUP BY "+year_column

            resultproxy2 = connection.execute(new_query)
            further_information = [{column: value for column, value in rowproxy.items()} for rowproxy in resultproxy2]
            response["further_information"] = further_information
            json_response = flask.jsonify(response)
            json_response.headers.add('Access-Control-Allow-Origin', '*')
            return json_response

        else:
            print("error", r.status_code)
            response = flask.jsonify({"error" : r.status_code})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
