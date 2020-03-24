from flask import Flask,request,jsonify,Response
#from flask_restful import Resource,Api
from prediction import prediction,test,tested
import pandas as pd
import pyodbc
import pandas.io.sql as psql
from model import current_developers
from get_data import dataframe,latest_defect,get_ticket_byId,paginated_tickets,update_developer
from flask_cors import CORS
import os
from os.path import join, dirname
from dotenv import load_dotenv
from model import run_model,missing_values_treatment
import json


load_dotenv()


app=Flask(__name__)
CORS(app)

DEBUG=eval(os.environ.get("DEBUG"))

PRODUCTION=eval(os.environ.get("PRODUCTION"))


PORT = int(os.environ.get("PORT"))

# connection_string=os.environ.get("CONNECTION_STRING")
# connection_string_local=os.environ.get("CONNECTION_STRING_LOCAL")

query="select top 3 * from [dbo].[tbl_Employee]"

@app.route('/',methods=['POST','GET'])
def home():
    return {"message":"sucesss"},200

@app.route('/data',methods=['POST','GET'])
def data():
    print("In Data API")
    #df=pd.read_sql(query,pyodbc.connect(connection_string))
    return {"message":"sucesss"},200

@app.route('/visualize',methods=['POST','GET'])
def visualize():
    dis={}
    dis['labels']=list(dataframe['Developer'][dataframe['Developer'].isin(current_developers)].value_counts().index.values)
    dis['values']=list(map(int,dataframe['Developer'][dataframe['Developer'].isin(current_developers)].value_counts().values))
    return {"labels":dis['labels'],"values":dis['values']},200 #pd.DataFrame(dis).to_json(),200

@app.route('/predict',methods=['POST','GET'])
def predict():
    #print("ticketdata:",ticketdata)
    #print(request.args)
    pagesize=request.args.get('pagesize',default=5,type=int)
    start=request.args.get('page',default=1,type=int)
    sortCol=request.args.get('sort_col',default='ID',type=str)
    sortDir=request.args.get('sort_dir',default='asc',type=str)
    search=request.args.get('search',default='%',type=str)
    startpage=int(pagesize)*(start-1)
    print(pagesize,start,startpage,sortCol,search,sortDir)
    if search=='':
        search='%'
    print("pagesize:",pagesize,"startpage:",startpage,"sortcol:",sortCol,"sortDir",sortDir,"search:",search)
    res,ticketscount=paginated_tickets(pagesize,sortCol,sortDir,search,startpage)
    #print(res)
    # if sortDir=='asc':
    #     sortDir=True
    # else:
    #     sortDir=False
    # #print(pagesize,start)
    # print("After Pagination")
    # #print("pagesize:",pagesize,"startpage:",startpage,"ticketdata:",ticketscount)
    # #paging_tickets=ticketdata.iloc[startpage:startpage+pagesize,:]
    
    # # print("missing Value treatment")
    # # treated_tickets=missing_values_treatment(paging_tickets)
    
    # # treated_tickets.drop('Developer',inplace=True,axis=1)
    # #print(treated_tickets['Title'])
    # #print(ticketdata['Title'])
    # #result=prediction(ticketdata)'Title',
    # print("working on paging data")
    # final_df=paging_tickets 
    # final_df['Developers']=final_df[['Developer1','Developer2','Developer3','Recommended']].apply(tested,axis=1)
    # #final_df['Developers']=list(final_df['Recommended'],final_df['Developer1'],final_df['Developer2'],final_df['Developer3'])
    # res=final_df[['Title','Developers','ID']].apply(test,axis=1)
    # #print(res)
    # print("response generation")
    #result.to_csv('data.csv')
    #return json.dumps({"results":list(res),"pagesize":ticketscount}),200
    #print({"results":{"Developers":list(res['Developers'].values),"Recommended":list(res['Recommended'].values),"Title":list(res['Title'].values),"ID":list(res['ID'].values)},"pagesize":int(ticketscount.iloc[0])})
    #return {"results":{"Developers":list(res['Developers'].values),"Recommended":list(res['Recommended'].values),"Title":list(res['Title'].values),"ID":list(res['ID'].values)},"pagesize":int(ticketscount.iloc[0])},200

    return {"results":list(res),"pagesize":int(ticketscount.iloc[0])}
    #return Response(result,mimetype='application/json')



@app.route('/view',methods=['POST','GET'])
def view():
    ticketdata=latest_defect()
    print("Before Prediction")
    global tickets
    tickets=len(ticketdata.index)
    result=prediction(ticketdata)
    #prediction(ticketdata)
    print("After Prediction")
    
    return {"results":result},200 if result=="sucess" else 500 


@app.route('/update',methods=['POST','GET'])
def update():
    Id=request.args.get('Id',type=int)
    Developer=request.args.get('selecteddeveloper',type=str)
    
    result=update_developer(Id,Developer)
    print("After update")
    return json.dumps({"results":result}),200


@app.route('/predicts',methods=['POST','GET'])
def predicts():
    print("Before Prediction")
    # print("missing Value treatment")
    # treated_tickets=missing_values_treatment(paging_tickets)
    ticketdata=latest_defect()
    # treated_tickets.drop('Developer',inplace=True,axis=1)
    #print(treated_tickets['Title'])
    #print(ticketdata['Title'])
    #result=prediction(ticketdata)
    global result
    result=prediction(ticketdata)
    print("After Prediction")
    return json.dumps({"results":result}),200
    #return {"results":result,"pagesize":pagesize}
    #return Response(result,mimetype='application/json')


@app.route('/recommendedDeveloper',methods=['POST','GET'])
def recommendedDeveloper():
    Id=request.args.get('Id',default='',type=int)
    if Id!='':
        result=get_ticket_byId(Id)
        #result=prediction(ticket)
        #print(result)
        return json.dumps({"results":list(result)}),200

@app.route('/runmodel',methods=['POST','GET'])
def runmodel():
    data=request.get_json()
    try:
        result=run_model(dataframe)
    except Exception as e:
        print(e)
        return {"model": "failed"},500
    else:
        #print("")
        return {"model":"Ran successfully"},200
    #return Response({"model":"Ran successfully"},200,mimetype='application/json')
    
    

if __name__ == "__main__":
    if(PRODUCTION):
        app.run()
        
    else:
       print("app running at port",PORT,"debug mode",DEBUG)
       app.run(port=PORT,debug=DEBUG)
