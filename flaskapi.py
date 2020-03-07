from flask import Flask,request,jsonify,Response
#from flask_restful import Resource,Api
from prediction import prediction
import pandas as pd
import pyodbc
import pandas.io.sql as psql
from model import current_developers
from get_data import dataframe
from flask_cors import CORS
import os
from os.path import join, dirname
from dotenv import load_dotenv
from model import run_model



load_dotenv()


app=Flask(__name__)
CORS(app)

DEBUG=eval(os.environ.get("DEBUG"))

PORT = int(os.environ.get("PORT"))

connection_string=os.environ.get("CONNECTION_STRING")

query="select top 3 * from [dbo].[tbl_Employee]"

@app.route('/',methods=['POST','GET'])
def data():
    return {"message":"sucesss"},200

@app.route('/data',methods=['POST','GET'])
def data():
    print("In Data API")
    df=pd.read_sql(query,pyodbc.connect(connection_string))
    return {"message":"sucesss"},200

@app.route('/visualize',methods=['POST','GET'])
def visualize():
    dis={}
    dis['labels']=list(dataframe['Developer'][dataframe['Developer'].isin(current_developers)].value_counts().index.values)
    dis['values']=list(map(int,dataframe['Developer'][dataframe['Developer'].isin(current_developers)].value_counts().values))
    return {"labels":dis['labels'],"values":dis['values']},200#pd.DataFrame(dis).to_json(),200

@app.route('/predict',methods=['POST','GET'])
def predict():
    data=request.get_json()
    print(data)
    print("Before Prediction")
    result=prediction(data)
    print("After Prediction")
    return Response(result,mimetype='application/json')

@app.route('/runmodel',methods=['POST','GET'])
def runmodel():
    data=request.get_json()
    run_model(dataframe)
    print("After Prediction")
    return Response({"model":"Ran successfully"},200,mimetype='application/json')
    
    

if __name__ == "__main__":
    if(DEBUG):
        print("app running at port",PORT,"debug mode",DEBUG)
        app.run(port=PORT,debug=DEBUG)
        
    else:
        print("app running at port",PORT,"debug mode",DEBUG)
        app.run(port=PORT)
