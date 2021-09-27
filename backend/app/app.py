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


@api.route("/ask-extended", methods=['GET'])
class AskExtendedToValueNet(Resource):
    def get(self):
        if 'question' in request.values:
            question = request.values["question"]
        else:
            question = "What is the share of electric cars in 2016 for Wetzikon?" 

        # Get SQL query
        payload = {'question': question}
        headers = {'Content-Type': 'application/json', "X-API-KEY": "sjNmaCtviYzXWlS"}
        r = requests.put("https://inference.hackzurich2021.hack-with-admin.ch/api/question/hack_zurich", headers=headers, data=json.dumps(payload)) 

        # Working queries:
        # Which municipality has the highest public transport share?
        # What is the share of electric cars in 2016 for Wetzikon?

        if r.status_code == 200:
            response = {}

            response["question"] = request.values["question"]
            

            # Get the «standard» data
            sql_statement = r.json()["sql"]
            resultproxy = connection.execute(sql_statement)
            standard_data = [{column: value for column, value in rowproxy.items()} for rowproxy in resultproxy]
            response["standard_data"] = standard_data
            response["standard_query"] = sql_statement
            print(sql_statement)

            # Set new query
            new_query = ""

            # Check if query with ORDER BY xxx LIMIT 1 
            pattern = re.search(r"(ORDER BY )([a-zA-Z1-9._]+) ((DESC)|(ASC))( LIMIT 1)", sql_statement)
            if pattern:
                order_by_criteria = pattern.group(2)
                start = sql_statement.split("FROM")[0]
                middle_part = sql_statement.split("FROM")[1].split("ORDER BY")[0]
                new_query = start+", "+order_by_criteria+" FROM "+middle_part

            # Check if FROM WHERE query
            pattern = re.search(r"(SELECT )([a-zA-Z1-9._]+)( FROM )([a-zA-Z1-9._\s=]+)( WHERE )([a-zA-Z1-90._\s=']+)", sql_statement)
            if pattern:
                # sql_statement = "SELECT T1.share_electric_cars FROM share_electric_cars AS T1 JOIN spatialunit AS T2 ON T1.spatialunit_id = T2.spatialunit_id WHERE T1.year = 2016 and T2.name = 'Wetzikon'       "
                m = re.search('(SELECT )([a-zA-Z1-9._]+)( FROM )', sql_statement)
                select_column = m.group(2)
                splitted_query = [string.split("FROM") for string in sql_statement.split("WHERE")]
                
                middle_query = splitted_query[0][1]
                if len(splitted_query[1][0].split(" and ")) > 1:
                    where_clause = " WHERE "+splitted_query[1][0].split(" and ")[1]
                else:
                    where_clause = ""
                year_column = splitted_query[1][0].split(" and ")[0].split(" = ")[0]
                new_query = "SELECT AVG("+select_column+"), "+year_column+" FROM "+middle_query+where_clause+" GROUP BY "+year_column

            if new_query:
                print(new_query)
                try:
                    resultproxy2 = connection.execute(new_query)
                except:
                    print("Query not callable")
                else:
                    further_information = [{column: value for column, value in rowproxy.items()} for rowproxy in resultproxy2]
                    response["further_information"] = further_information
                    response["further_query"] = new_query
                    print(further_information)
                
                

            # SELECT T1.name FROM spatialunit AS T1 ORDER BY T1.area DESC LIMIT 1
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
