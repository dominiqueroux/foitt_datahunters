#!/usr/bin/python
### reads all files from the directorz of certain type (csv/json) and 
### converts it to the SQL file with create and insert statements

import pandas as pd
import json
from os import listdir
from os.path import isfile, join


def SQL_INSERT_STATEMENT_FROM_DATAFRAME(SOURCE, TARGET):
    sql_texts = []
    for index, row in SOURCE.iterrows():
        sql_texts.append('INSERT INTO "'+TARGET+'" ("index", "'+ str('", "'.join(SOURCE.columns))+ '") VALUES  '+ str((index,)+tuple(row.values)).replace("nan","null")+";")
    return sql_texts

sourcetyp="csv" #csv or json
mypath="./input"+sourcetyp+"/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for file in onlyfiles:
    if sourcetyp == "csv":
        raw_data = pd.read_csv(mypath+file)
    else:
        jsonfile=open(mypath+file, 'r')
        data=jsonfile.read()
        obj = json.loads(data)
        raw_data = pd.DataFrame.from_dict(pd.json_normalize(obj))
    
    tablename = file.split("."+sourcetyp)[0]
    sql_text = []
    sql_text.append(pd.io.sql.get_schema(raw_data.reset_index(), tablename)+";")  #gen create statement
    sql_text.append("\n")
    sql_text = sql_text + SQL_INSERT_STATEMENT_FROM_DATAFRAME(raw_data, tablename)
    sql_text.append("\n\n")

    outputsql = open('out'+sourcetyp+'.sql', 'a')
    for element in sql_text:
        print(element, file=outputsql)
    outputsql.close()
