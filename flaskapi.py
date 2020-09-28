from flask import Flask,request,jsonify,Response
#from flask_restful import Resource,Api
from prediction import prediction,test,tested
import pandas as pd
import pyodbc
import pandas.io.sql as psql
from model import current_developers
from get_data import dataframe,latest_defect,get_ticket_byId,paginated_tickets,update_developer,pull_data_bydate,pull_data,store_data,getticket_databyId
from flask_cors import CORS
import os
from os.path import join, dirname
from dotenv import load_dotenv
from model import run_model,missing_values_treatment,evaluation
from utils.utilfunctions import seggregation,formatseveritylist
import json
from fuzzywuzzy import fuzz
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import *

load_dotenv()

df=pd.DataFrame({'a':[1,2,3,4,5],'b':[9,8,7,6,5],'c':[6,4,5,6,7]})
ticketMail=pd.DataFrame({})

# message=Mail(
#     from_email='divakarkareddy@gmail.com',
#     to_emails='dinu818690@gmail.com',
#     subject='Recommendations Mail',
#     html_content=sendmail(df),
# )

# sendgrid=SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

# res=sendgrid.send(message)

# print(res.status_code,res.headers)
# if res.status_code=='200':
#     print("Mail send")

load_dotenv()

app=Flask(__name__)
CORS(app)

DEBUG=eval(os.environ.get("DEBUG"))

PRODUCTION=eval(os.environ.get("PRODUCTION"))

FILE_FOLDER_PATH=os.environ.get("FILE_UPLOAD")


PORT = int(os.environ.get("PORT"))

SIMILARITY_PERCENT=float(int(os.environ.get('SIMILARITY_PERCENT')))

# connection_string=os.environ.get("CONNECTION_STRING")
# connection_string_local=os.environ.get("CONNECTION_STRING_LOCAL")

query="select top 3 * from [dbo].[tbl_Employee]"


###########################  ----- Home ----#####################
@app.route('/',methods=['POST','GET'])
def home():
    return {"message":"sucesss"},200

###########################  ----- data ----#####################
@app.route('/data',methods=['POST','GET'])
def data():
    print("In Data API")
    #df=pd.read_sql(query,pyodbc.connect(connection_string))
    return {"message":"sucesss"},200

###########################  ----- Visualize ----#####################
@app.route('/visualize',methods=['POST','GET'])
def visualize():
    startDate=request.args.get('startDate',default='',type=str)
    endDate=request.args.get('endDate',default='',type=str)
    #print("startDate",startDate)
    if(startDate):
        if(endDate):
            visualdataframe,vis=pull_data_bydate(startDate,endDate)
        else:
            visualdataframe,vis=pull_data_bydate(startDate,'')
    elif(endDate):
        visualdataframe,vis=pull_data_bydate('',endDate)
    else:
        visualdataframe,vis=pull_data_bydate('','')
    if len(visualdataframe.index)==0:
        return {}
    visualdataframe[['Seggregation','Application']]=pd.DataFrame(visualdataframe[['Title','Module']].apply(seggregation,axis=1))
    #print(visualdataframe.head(50))
    line={}
    visualdataframe.sort_values(by='Developer',ascending=True,inplace=True)
    line['labels']=list(visualdataframe['Developer'][visualdataframe['Developer'].isin(current_developers)].value_counts().index.values)
    line['values']=list(map(int,visualdataframe['Developer'][visualdataframe['Developer'].isin(current_developers)].value_counts().values))
    devvisualdf=visualdataframe[visualdataframe['Developer'].isin(current_developers)]
    devvisualdf=pd.DataFrame(devvisualdf.groupby(['Developer','Severity']).count()['ID']).reset_index()
    devvisualdf.sort_values(by='Developer',ascending=True,inplace=True)
    devvisualdf['List']=devvisualdf[['Severity','ID']].apply(formatseveritylist,axis=1)
    devp=[]
    sevl=[]
    for i in sorted(current_developers):
        devp.append(i)
        sevl.append(list(devvisualdf[devvisualdf['Developer']==i]['List'].values))
    line['drilllabels']=devp
    line['drillvalues']=sevl
    bar={}
    bar['labels']=list(visualdataframe['Application'].value_counts().index)
    bar['values']=list(map(int,visualdataframe['Application'].value_counts().values))
    
    labels={}
    values={}
    vdf=pd.DataFrame(visualdataframe.groupby(['Application','Seggregation']).count()['ID']).reset_index()
    labels['billinglabels']=list(vdf[vdf['Application']=='Billing']['Seggregation'].values)
    labels['policylabels']=list(vdf[vdf['Application']=='Policy']['Seggregation'].values)
    labels['claimslabels']=list(vdf[vdf['Application']=='Claims']['Seggregation'].values)
    labels['partylabels']=list(vdf[vdf['Application']=='Party']['Seggregation'].values)
    labels['otherlabels']=list(vdf[vdf['Application']=='Other']['Seggregation'].values)
    values['billingvalues']=list(map(str,vdf[vdf['Application']=='Billing']['ID'].values))
    values['policyvalues']=list(map(str,vdf[vdf['Application']=='Policy']['ID'].values))
    values['claimsvalues']=list(map(str,vdf[vdf['Application']=='Claims']['ID'].values))
    values['partyvalues']=list(map(str,vdf[vdf['Application']=='Party']['ID'].values))
    values['othervalues']=list(map(str,vdf[vdf['Application']=='Other']['ID'].values))
    labels['appnames']=list(pd.DataFrame(visualdataframe.groupby(['Application']).count())['ID'].index)
    values['appvalues']=list(map(str,pd.DataFrame(visualdataframe.groupby(['Application']).count())['ID'].values))
    defectschart={}
    # dataframe['createdDate2']=dataframe['Created Date'].dt.strftime('%Y-%m')
    # dataframe.sort_values(['createdDate2'],ascending=False,inplace=True)
    defectschart['labels']=list(vis['createdDate2'].values)
    defectschart['values']={"all":list(map(int,vis['All'].values)),"policy":list(map(int,vis['Policy'].values)),"billing":list(map(int,vis['Billing'].values)),"claims":list(map(int,vis['Claims'].values)),"other":list(map(int,vis['Other'].values))}

    pie={}
    #visualdf=pd.DataFrame(visualdataframe.groupby(['Application','Severity']).sum()['Percent']).reset_index()
    pie['labels']=list(visualdataframe['Application'].value_counts().index)
    pie['values']=list(map(int,visualdataframe['Application'].value_counts().values))
    appdf=pd.DataFrame(visualdataframe.groupby(['Application','Severity']).count()['ID']).reset_index()
    appdf['SeverityList']=appdf[['Severity','ID']].apply(formatseveritylist,axis=1)
    devp=[]
    sevl=[]
    for i in sorted(appdf['Application'].unique()):
        devp.append(i)
        sevl.append(list(appdf[appdf['Application']==i]['SeverityList'].values))
    pie['drilllabels']=devp
    pie['drillvalues']=sevl


    defectsdata={}
    df=visualdataframe.copy()

    ls=list(df.groupby('Module').count()[df.groupby('Module').count()['Severity']<10].index)
    df['Module']=df['Module'].replace(ls,'Others')
    df['Module']=df['Module'].replace('','Unknown')
    defectsdata['labels']=list(df['Module'].value_counts().index)
    defectsdata['values']=list(map(int,df['Module'].value_counts().values))
    #print(defectsdata)
    return {"line_data":{"labels":line['labels'],"values":line['values'],"drilllabels":line['drilllabels'],"drillvalues":line['drillvalues']},
    "bar_data":{"labels":labels,"values":values},
    "defectschart_data":{"labels":defectschart['labels'],"values":defectschart['values']},
    "pie_data":{"labels":pie['labels'],"values":pie['values'],"drilllabels":pie['drilllabels'],"drillvalues":pie['drillvalues']},
    "defects_data":{"labels":defectsdata['labels'],"values":defectsdata['values']}},200 #pd.DataFrame(dis).to_json(),200

###########################  ----- Predict ----#####################
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
    if search=='':
        search='%'
    #print("pagesize:",pagesize,"startpage:",startpage,"sortcol:",sortCol,"sortDir",sortDir,"search:",search)
    res,ticketscount,df=paginated_tickets(pagesize,sortCol,sortDir,search,startpage)
    global ticketMail
    ticketMail=df[['ID','Title','Recommended','Developer1','Developer2','Developer3']]
    ticketMail.columns=['ID','Ticket Description','Assigned','Developer1','Developer2','Developer3']
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

###########################  ----- View ----#####################
@app.route('/recommendations',methods=['POST','GET'])
def view():
    ticketdata=latest_defect()
    # print("Before Prediction")
    global tickets
    tickets=len(ticketdata.index)
    result=prediction(ticketdata)
    #prediction(ticketdata)
    # print("After Prediction")
    
    return {"results":result},200 if result=="sucess" else 500 

###########################  ----- Update ----#####################
@app.route('/update',methods=['POST','GET'])
def update():
    Id=request.args.get('Id',type=int)
    Developer=request.args.get('selecteddeveloper',type=str)
    
    result=update_developer(Id,Developer)
    print("After update")
    return json.dumps({"results":result}),200

###########################  ----- Predicts ----#####################
# @app.route('/predicts',methods=['POST','GET'])
# def predicts():
#     print("Before Prediction")
#     # print("missing Value treatment")
#     # treated_tickets=missing_values_treatment(paging_tickets)
#     ticketdata=latest_defect()
#     # treated_tickets.drop('Developer',inplace=True,axis=1)
#     #print(treated_tickets['Title'])
#     #print(ticketdata['Title'])
#     #result=prediction(ticketdata)
#     global result
#     result=prediction(ticketdata)
#     print("After Prediction")
#     return json.dumps({"results":result}),200
#     #return {"results":result,"pagesize":pagesize}
#     #return Response(result,mimetype='application/json')

###########################  ----- Recommended Developer ----#####################
@app.route('/recommendedDeveloper',methods=['POST','GET'])
def recommendedDeveloper():
    Id=request.args.get('Id',default='',type=int)
    if Id!='':
        result=get_ticket_byId(Id)
        #result=prediction(ticket)
        #print(result)
        return json.dumps({"results":list(result)}),200

@app.route('/similardefects',methods=['POST','GET'])
def similardefects():
    pagesize=request.args.get('pagesize',default=5,type=int)
    start=request.args.get('page',default=1,type=int)
    sortCol=request.args.get('sort_col',default='similarityscore',type=str)
    if(sortCol=='Id'):
        sortCol='ID'
    sortDir=request.args.get('sort_dir',default='asc',type=str)
    search=request.args.get('search',default='',type=str)
    if(search==''):
        print('no results')
        return {'results':[{'id':list(),'title':list(),'similarityscore':list()}],'pageSize':0}
    startpage=int(pagesize)*(start-1)
    #dataframe=pull_data()
    dataframe['similarityscore']=dataframe['Title'].apply(lambda x:fuzz.token_sort_ratio(x,search))
    dataframe.sort_values(by='similarityscore',ascending=False,inplace=True)
    #print(SIMILARITY_PERCENT)
    data=dataframe[dataframe['similarityscore']>SIMILARITY_PERCENT].copy()
    if(sortDir=='asc'):
        data.sort_values(by=sortCol,inplace=True)
    else:
        data.sort_values(by=sortCol,ascending=False,inplace=True)
    count=len(data.index)
    #print("print dataframe")
    #data=data.iloc[:,[0,1,8]]
    data=data.iloc[startpage:startpage+pagesize]
    #print(data)
    results=[]
    for i,j,k in zip(data['ID'],data['Title'],data['similarityscore']):
        dis={}
        dis['id']=i
        dis['title']=j
        dis['similarityscore']=k
        results.append(dis)
    #print(data)
    return {'results':results,'pageSize':count}
    #return {'results':{'id':list(map(str,data['ID'].values)),'title':list(data['Title'].values),'similarityscore':list(map(str,data['similarityscore'].values)),'pageSize':count}}

@app.route('/ticketDetails',methods=['GET','POST'])
def ticketDetails():
    ticketId=request.args.get('ticketId',default=0,type=int)
    ticketdata,res=getticket_databyId(ticketId)
    result=ticketdata.to_json(orient='records')
    return {'results':res}

@app.route('/currentDevelopers',methods=['GET','POST'])
def currentDevelp():
    #print("current developers",current_developers)
    return {'results':list(current_developers)}

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

@app.route('/evaluation',methods=['POST','GET'])
def evaluation1():
    #data=request.get_json()
    try:
        result=evaluation(dataframe)
    except Exception as e:
        print(e)
        return {"model": "failed"},500
    else:
        return {"model":result},200


@app.route('/sendmail',methods=['POST','GET'])
def sendmail():
    fromEmail=request.args.get('from',default='',type=str)
    toEmail=request.args.get('to',default='',type=str)
    subject=request.args.get('subject',default="tickets data",type=str)
    toname=request.args.get('name',default="Divakar",type=str)
    fromname=request.args.get('name',default="Manager",type=str)
    sendgrid=SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    table=ticketMail.to_html()

    email_content='''<p>Hi {Toname},</p><br><br>
    <p>Please find the attached list of tickets and recommended developers</p>
    {table}
    <p>Please visit the following link to update the developer of a ticket
    <a href='http://localhost:4200/#/tickets'>Update developer in ticket dashboard</a> </p>
    <br>
    <br>
    <br>
    Regards,
    {FromName}
    
    '''.format(table=table,Toname=toname,FromName=fromname)
    # mail_html =str(prolog+ticketMail.to_html()+epilog)
    # mail_txt = 'This is a test email message.'
    #mail_html = Content('text/html',prolog+'<br>'+ticketMail.to_html()+'<br>'+epilog)
    #mail_txt = Content('This is a test email message.','text/plain')
    message=Mail(
    from_email=fromEmail,
    to_emails=toEmail,
    subject=subject,
    html_content=email_content
    )
    #message.add_content('This is a test email message.','text/plain')
    #res=sendgrid.send(message)
    res=sendgrid.client.mail.send.post(request_body=message.get())
    print("Response ",res.status_code)
    if(res.status_code==200 or res.status_code==202):
        return {'results':'Mail Sent Successfully!'}#render_template('email.html',column_names=df.columns.values,row_data=list(df.values.tolist()))
    else:
        return {'results':res.error}

@app.route("/UploadFile", methods=["GET", "POST","PUT"])
def uploadFile():
    project=request.args.get('project',default='',type=str)
    #file=request.args.get('File',default='',type=str)
    #print(request)
    print(project)
    if request.method == "POST" or request.method == "PUT":
        if request.files:
            file = request.files["File"]            
            file.save(file.filename)
            df=pd.DataFrame({})
            #try:
            if('.xlsx' in file.filename or '.xls' in file.filename):
                df=pd.read_excel(file.filename)
                df_old=pull_data()
                df=pd.concat([df_old,df])
                df['Project_Id']=project
                df.drop_duplicates(inplace=True)
                #df.columns=['ID','Title','State','Developer','Module','Severity','Tester','Created Date','Root Cause','Project_Id']
                os.remove(file.filename)
                df['CreatedDate']=pd.to_datetime(df['CreatedDate']).dt.strftime("%Y-%m-%d")
                store_data('TicketHistory',df,'replace')
            elif('.csv' in file.filename):
                print(file.filename)
                df=pd.read_csv(file.filename)
                df_old=pull_data()
                df=pd.concat([df_old,df])
                df['Project_Id']=project
                df.drop_duplicates(inplace=True)
                os.remove(file.filename)
                #df.columns=['ID','Title','State','Developer','Module','Severity','Tester','Created Date','Root Cause','Project_Id']                    
                #df['CreatedDate']=pd.to_datetime(df['CreatedDate']).dt.strftime("%Y-%m-%d")
                store_data('TicketHistory',df,'replace')
            #except Exception as e:
                #print(e)
            #return {'results':'failed to store in database because of '+str(e)}
        else:
            return {'results':'error'}                                       
    return {'results':'success'}


if __name__ == "__main__":
    if(PRODUCTION):
        app.run()   
    else:
       print("app running at port",PORT,"debug mode",DEBUG)
       app.run(port=PORT,debug=DEBUG)
