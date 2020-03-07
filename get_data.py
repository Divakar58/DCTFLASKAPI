import pyodbc
import pandas as pd
import pandas.io.sql as psql
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()

connection_string=os.environ.get("CONNECTION_STRING")
query=os.environ.get("TKTS_QUERY")

# def connect(connection_string):
#     connection=pyodbc.connect(connection_string)
#     return connection

#print(connection_string)

def pull_data():
    #connection=pyodbc.connect(connection_string)
    #df=pd.read_sql(query,connection)
    #connection.close()
    
    df=pd.DataFrame({'Title':['Coverage Match','TransACT page RSOD'],'Id':[1,2]})
    return df

dataframe=pull_data()


