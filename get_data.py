import pyodbc
import pandas as pd
import pandas.io.sql as psql
import os
from dotenv import load_dotenv
import urllib
from sqlalchemy import create_engine
from datetime import date
import ast

load_dotenv()


drivers= [driver for driver in pyodbc.drivers()]
# print(drivers)
#connection_string="DRIVER={"+drivers[0]+"};SERVER=tcp:duckdb.database.windows.net,1433;DATABASE=ACRF;UID=dct;PWD=Duck@123;Encrypt=yes;TrustServerCertificate=no;"

production=ast.literal_eval(os.environ.get("PRODUCTION"))
connection_string=os.environ.get("CONNECTION_STRING")
connection_string_local=os.environ.get("CONNECTION_STRING_LOCAL")
query=os.environ.get("TKTS_QUERY")
latestquery=os.environ.get("LATEST_TICKETS")
currentdevelopers=os.environ.get("CURRENT_DEVELOPERS")



def test(a):
    lis=[]
    for i in a:
        lis.append(i)
    return lis
# def connect(connection_string):
#     connection=pyodbc.connect(connection_string)
#     return connection

#print(connection_string)
def store_data(table,df):
    if(production):
        quoted = urllib.parse.quote_plus(connection_string)
    else:
        quoted = urllib.parse.quote_plus(connection_string_local)
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
    df.drop_duplicates(inplace=True)
    df.sort_values(by='ID',inplace=True)
    df=df.set_index('ID')
    df.to_sql(table, schema='dbo', con = engine, if_exists='append')


def pull_data():
    if(production):
        connection=pyodbc.connect(connection_string)
    else:
        connection=pyodbc.connect(connection_string_local)
    tickethistoryquery=query+"where project_Id=1"
    df=pd.read_sql(tickethistoryquery,connection)
    connection.close()
    #df=pd.DataFrame({'Title':['Coverage Match','TransACT page RSOD'],'Id':[1,2]})
    return df

def module_allocation(x):
    if 'policy' in x.lower():
        return "Policy"
    elif 'billing' in x.lower():
        return "Billing"
    elif 'claims' in x.lower():
        return "Claims"
    else:
        return "Other"

def pull_data_bydate(startDate,endDate):
    if(production):
        connection=pyodbc.connect(connection_string)
    else:
        connection=pyodbc.connect(connection_string_local)
    querydate=os.environ.get("TKTS_QUERY_BYDATE")
    #print(querydate)
    # print("startDate=",startDate,"endDate=",endDate)
    if(startDate!=''):
        if(endDate!=''):
            querydate=querydate+" where [CreatedDate]> '"+ startDate+ "' and [CreatedDate]<'"+endDate+"'"
            print(querydate)
        else:
            querydate=querydate+" where [CreatedDate]> '"+ startDate +"'"
            print(querydate)
    else:
        querydate=querydate
    # print(querydate)
    df=pd.read_sql(querydate,connection)
    connection.close()
    # print(df.head())

    df['createdDate2']=pd.to_datetime(df['CreatedDate']).dt.strftime('%Y-%m')
    df.sort_values('createdDate2',ascending=False,inplace=True)
    df['Stream']=df['Module'].apply(module_allocation)
    df['Created Date']=pd.to_datetime(df['CreatedDate'],dayfirst=True)#.dt.date
    k=pd.DataFrame(df.groupby(['createdDate2']).count()['ID'].reset_index())
    a=pd.DataFrame(df[df['Stream']=='Policy'].groupby(['createdDate2']).count()['ID'].reset_index())
    b=pd.DataFrame(df[df['Stream']=='Billing'].groupby(['createdDate2']).count()['ID'].reset_index())
    c=pd.DataFrame(df[df['Stream']=='Claims'].groupby(['createdDate2']).count()['ID'].reset_index())
    d=pd.DataFrame(df[df['Stream']=='Other'].groupby(['createdDate2']).count()['ID'].reset_index())
    temp=pd.merge(k,a,on='createdDate2',how='left',suffixes=('_all', '_policy'))
    temp1=pd.merge(temp,b,on='createdDate2',how='left')
    temp2=pd.merge(temp1,c,on='createdDate2',how='left',suffixes=('_billing', '_claims'))
    temp3=pd.merge(temp2,d,on='createdDate2',how='left')
    temp3.fillna(0,inplace=True)
    temp3.rename({'ID_all':'All','ID_policy':'Policy','ID_billing':'Billing','ID_claims':'Claims','ID':'Other'},axis=1,inplace=True)
    #print(df)
    return df,temp3

def get_ticket_byId(id):
    if(production):
        connection=pyodbc.connect(connection_string)
    else:
        connection=pyodbc.connect(connection_string_local)
    #df=pd.read_sql(latestquery+"where Id="+str(id),connection)
    df=pd.read_sql("SELECT * from RecommendationsData where Id="+str(id),connection)
    connection.close()
    #df=pd.DataFrame({'Title':['Coverage Match','TransACT page RSOD'],'Id':[1,2]})
    df=format_response(df,'notrecommend')
    return df
def update_developer(Id,developer):
    if(production):
        connection=pyodbc.connect(connection_string)
    else:
        connection=pyodbc.connect(connection_string_local)
    updatequery="Update RecommendationsData set  Recommended='"+str(developer)+"' where ID="+str(Id)
    # print(query)
    cursor=connection.cursor()
    cursor.execute(updatequery)
    cursor.commit()
    # try:
    #     cursor.execute(query)
    #     cursor.commit()
    # except Exception as e:
    #     raise Exception("Update failed")
    cursor.close()
    return "Updated Successfully!"
def get_current_developers():
    if(production):
        connection=pyodbc.connect(connection_string)
    else:
        connection=pyodbc.connect(connection_string_local)
    df=pd.read_sql(currentdevelopers,connection)
    # print(df)
    connection.close()
    return df['Name'].values

def format_response(final_df,type='recommended'):
    if(type=='recommended'):
        final_df['Developers']=final_df[['Developer1','Developer2','Developer3','Recommended']].apply(test,axis=1)
        
    else:
        final_df['Developers']=final_df[['Developer1','Developer2','Developer3']].apply(test,axis=1)
    #final_df['Developers']=list(final_df['Recommended'],final_df['Developer1'],final_df['Developer2'],final_df['Developer3'])
    final_df['Recommended']=final_df[['Recommended']].apply(test,axis=1)
    res=final_df[['Title','Developers','ID','Recommended']].apply(test,axis=1)
    #res=final_df
    return res

def latest_defect(search='%'):
    if(production):
        connection=pyodbc.connect(connection_string)
    else:
        connection=pyodbc.connect(connection_string_local)
    df=pd.read_sql(latestquery+"where [Title] like '%"+search+"%'",connection)
    connection.close()
    #df=pd.DataFrame({'Title':['Coverage Match','TransACT page RSOD'],'Id':[1,2]})
    #print(df.head())
    return df

def paginated_tickets(pagesize,sortCol,sortDir,search,startpage):
    if(production):
        connection=pyodbc.connect(connection_string)
    else:
        connection=pyodbc.connect(connection_string_local)
    pagequery="SELECT * FROM  (SELECT [index],ID, isnull(Title,'''') as Title, isnull(Developer1,'''') as Developer1,isnull(Developer2,'''') as Developer2,isnull(Developer3,'''') as Developer3,isnull(Recommended,'''') as Recommended from RecommendationsData where Title like '%"+search+"%') As TicketRows  WHERE ([index] >("+str(startpage)+") AND [index]<= "+str(startpage+pagesize )+") ORDER BY "+sortCol+" "+sortDir+";"
    searchquery="select * from (SELECT ROW_NUMBER() OVER (ORDER BY "+sortCol+" "+sortDir+") AS Row,ID, isnull(Title,'''') as Title, isnull(Developer1,'''') as Developer1,isnull(Developer2,'''') as Developer2,isnull(Developer3,'''') as Developer3,isnull(Recommended,'''') as Recommended from RecommendationsData where Title like '%"+search+"%') As TicketRows WHERE (Row >"+str(startpage)+" AND Row<= "+str(startpage+pagesize )+") ORDER BY "+sortCol+" "+sortDir+";"
    pagequery=searchquery if search!='%' else pagequery
    df=pd.read_sql(pagequery,connection)
    count_query="Select count(*) from RecommendationsData where Title like '%"+search+"%'"
    #print(query)
    count=pd.read_sql(count_query,connection)
    df1=df.copy()
    formated_df=format_response(df,type='recommended')
    return formated_df,count,df1

dataframe=pull_data()


