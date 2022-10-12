# required libraries
#import pyodbc
import pandas as pd
#import pandas.io.sql as psql
import numpy as np
from warnings import filterwarnings
filterwarnings('ignore')
#import matplotlib.pyplot as plt
#import seaborn as sns
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem import wordnet, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.pipeline import Pipeline
#from imblearn.pipeline import make_pipeline
#from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
#from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
#import xgboost
import re
import pickle
#from prediction import modelling
#import xgboost as xgb
#from xgboost import XGBClassifier
from get_data import dataframe,get_current_developers,get_current_developer_bystream
from sklearn.metrics import classification_report,accuracy_score
from utils.utilfunctions import seggregation,Estimation,missing_values_treatment
stream={'Billing':'1','Claims':'2','Policy':'3'}


current_developers=get_current_developers()
current_testers=get_current_developers(profile=2)
#print("current developers",current_developers)
Num_developer=3


def load_data(file):
    if re.search('/.xlsx$',flags=re.IGNORECASE):
        return pd.read_excel(file)
    elif re.search('/.csv$',flags=re.IGNORECASE):
        return pd.read_csv(file)
    else:
        return "invalid file format send in csv or xlsx format"

# def missing_values_treatment(dataframe):
#     dataframe['Developer'][dataframe['Developer'].isna()]='No Developer'
#     dataframe['Severity'][dataframe['Severity'].isna()]='2 - Medium'
#     dataframe['Estimate'][dataframe['Estimate'].isna()]=None
#     return dataframe

# def get_current_developer():
#     return current_developer

def current_developer(dataframe,current_developers):
    
    return dataframe[dataframe['Developer'].isin(current_developers)]
    #return dataframe.head(500)


def current_tester(dataframe,current_testers):
    
    return dataframe[dataframe['Tester'].isin(current_testers)]
    #return dataframe.head(500)

def devmodelling(dataframe):
    print("Developer modelling")
    #X=dataframe['Title']+' '+dataframe['Application']+' '+dataframe['Seggregation']
    X=dataframe['Title']#+' '+dataframe['Seggregation']
    y=dataframe['Developer']
    #X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0,random_state=42)
    print(dataframe.head())
    tcv=CountVectorizer(analyzer=text_process)
    tfv=TfidfTransformer()
    sm=SMOTE(k_neighbors=1,n_jobs=-1)#k_neighbors=3,
    svc=SVC(kernel='rbf',probability=True)
    #mb=MultinomialNB()
    rfc=RandomForestClassifier()
    xgc=XGBClassifier()
    print("before pipe")
    pipe=make_pipeline(tcv,tfv,sm,xgc)
    #pipe=make_pipeline(tcv,tfv,mb)
    #pipe.fit(X=X_train,y=y_train)
    pipe.fit(X,y)
    return pipe
def estmodelling(dataframe):
    print("Estimate modelling")
    #print(dataframe.columns)
    X=dataframe['Title']+' '+dataframe['Application']+' '+dataframe['Seggregation']
    y=dataframe['Complexity']
    #print(dataframe.isna().sum())
    #X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0,random_state=42)
    tcv=CountVectorizer(analyzer=text_process)
    tfv=TfidfTransformer()
    sm=SMOTE(k_neighbors=1,n_jobs=-1)#k_neighbors=3,
    svc=SVC(kernel='rbf',probability=True)
    #mb=MultinomialNB()
    rfc=RandomForestClassifier()
    xgc=XGBClassifier()
    print("before pipe")
    pipe=make_pipeline(tcv,tfv,sm,xgc)
    print("after pipe")
    #pipe=make_pipeline(tcv,tfv,mb)
    #pipe.fit(X=X_train,y=y_train)
    print(X.isna().sum())
    print(dataframe[y.isna()])
    pipe.fit(X,y)
    return pipe
def testmodelling(dataframe):
    print("Tester modelling")
    #X=dataframe['Title']+' '+dataframe['Application']+' '+dataframe['Seggregation']
    X=dataframe['Title']#+' '+dataframe['Seggregation']
    y=dataframe['Tester']
    #X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0,random_state=42)
    print(dataframe.head())
    tcv=CountVectorizer(analyzer=text_process)
    tfv=TfidfTransformer()
    sm=SMOTE(k_neighbors=1,n_jobs=-1)#k_neighbors=3,
    svc=SVC(kernel='rbf',probability=True)
    #mb=MultinomialNB()
    rfc=RandomForestClassifier()
    xgc=XGBClassifier()
    print("before pipe")
    pipe=make_pipeline(tcv,tfv,sm,xgc)
    #pipe=make_pipeline(tcv,tfv,mb)
    #pipe.fit(X=X_train,y=y_train)
    pipe.fit(X,y)
    return pipe

def devevaluationagr(dataframe,projectid):
    print("evaluation")
    try:
        dataframe=missing_values_treatment(dataframe)
        dataframe[['Seggregation','Application']]=pd.DataFrame(dataframe[['Title','Module']].apply(seggregation,axis=1))
        dataframe['Complexity']=pd.DataFrame(dataframe[['Severity','Estimate']].apply(Estimation,axis=1))
        dummydf=dataframe.copy()
    except Exception as e:
        print(e)
        raise Exception 
        return {"message":"error"}
    accuracy=0
    for i in stream.items():
        streamdeveloper=get_current_developer_bystream(i[1],projectid)
        dummydf=current_developer(dataframe,streamdeveloper)
        print(dataframe.head())
        # dataframe=current_developer(dataframe,current_developers)
        X=dummydf['Title']+' '+dummydf['Seggregation']
        y=dummydf['Developer']
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)
        tcv=CountVectorizer(analyzer=text_process)
        tfv=TfidfTransformer()
        sm=SMOTE(k_neighbors=1,n_jobs=-1)
        svc=SVC(kernel='rbf',probability=True)
        rfc=RandomForestClassifier()
        #mb=MultinomialNB()
        xgc=XGBClassifier()
        pipe=make_pipeline(tcv,tfv,sm,xgc)
        #pipe=make_pipeline(tcv,tfv,mb)
        pipe.fit(X=X_train,y=y_train)
        y_predict=pipe.predict(X_test)
        print(classification_report(y_test,y_predict))
        print("Accuracy",round(accuracy_score(y_test,y_predict)*100,2))
        accuracy=accuracy+round(accuracy_score(y_test,y_predict)*100,2)
    return round(accuracy/len(stream),2)

def testevaluationagr(dataframe,projectid):
    print("test evaluation")
    try:
        dataframe=missing_values_treatment(dataframe)
        dataframe[['Seggregation','Application']]=pd.DataFrame(dataframe[['Title','Module']].apply(seggregation,axis=1))
        dataframe['Complexity']=pd.DataFrame(dataframe[['Severity','Estimate']].apply(Estimation,axis=1))
        dummydf=dataframe.copy()
    except Exception as e:
        print(e)
        raise Exception 
        return {"message":"error"}
    accuracy=0
    for i in stream.items():
        streamdeveloper=get_current_developer_bystream(i[1],projectid,profile=2)
        dummydf=current_tester(dataframe,streamdeveloper)
        print(dataframe.head())
        X=dummydf['Title']+' '+dummydf['Seggregation']
        y=dummydf['Tester']
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)
        tcv=CountVectorizer(analyzer=text_process)
        tfv=TfidfTransformer()
        sm=SMOTE(k_neighbors=1,n_jobs=-1)
        svc=SVC(kernel='rbf',probability=True)
        rfc=RandomForestClassifier()
        #mb=MultinomialNB()
        xgc=XGBClassifier()
        pipe=make_pipeline(tcv,tfv,sm,xgc)
        #pipe=make_pipeline(tcv,tfv,mb)
        pipe.fit(X=X_train,y=y_train)
        y_predict=pipe.predict(X_test)
        print(classification_report(y_test,y_predict))
        print("Accuracy",round(accuracy_score(y_test,y_predict)*100,2))
        accuracy=accuracy+round(accuracy_score(y_test,y_predict)*100,2)
    return round(accuracy/len(stream),2)

def devevaluation(dataframe):
    print("evaluation")
    try:
        dataframe=missing_values_treatment(dataframe)
        dataframe[['Seggregation','Application']]=pd.DataFrame(dataframe[['Title','Module']].apply(seggregation,axis=1))
        dataframe['Complexity']=pd.DataFrame(dataframe[['Severity','Estimate']].apply(Estimation,axis=1))
    except Exception as e:
        print(e)
        raise Exception 
        return {"message":"error"} 
    dataframe=current_developer(dataframe,current_developers)
    X=dataframe['Title']+' '+dataframe['Application']+' '+dataframe['Seggregation']
    y=dataframe['Developer']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)
    tcv=CountVectorizer(analyzer=text_process)
    tfv=TfidfTransformer()
    sm=SMOTE(k_neighbors=1,n_jobs=-1)
    svc=SVC(kernel='rbf',probability=True)
    rfc=RandomForestClassifier()
    #mb=MultinomialNB()
    xgc=XGBClassifier()
    pipe=make_pipeline(tcv,tfv,sm,xgc)
    #pipe=make_pipeline(tcv,tfv,mb)
    pipe.fit(X=X_train,y=y_train)
    y_predict=pipe.predict(X_test)
    print(classification_report(y_test,y_predict))
    print("Accuracy",accuracy_score(y_test,y_predict))
    return round(accuracy_score(y_test,y_predict)*100,2)

def estevaluationagr(dataframe,projectid):
    print("evaluation")
    try:
        dataframe=missing_values_treatment(dataframe)
        dataframe[['Seggregation','Application']]=pd.DataFrame(dataframe[['Title','Module']].apply(seggregation,axis=1))
        dataframe['Complexity']=pd.DataFrame(dataframe[['Severity','Estimate']].apply(Estimation,axis=1))
        dummyf=dataframe.copy()
    except Exception as e:
        return {"message":"error"} 
    accuracy=0
    for i in stream.items():
        streamdeveloper=get_current_developer_bystream(i[1],projectid)
        dummyf=current_developer(dataframe,streamdeveloper)
        X=dummyf['Title']+' '+dummyf['Seggregation']
        y=dummyf['Complexity']
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)
        tcv=CountVectorizer(analyzer=text_process)
        tfv=TfidfTransformer()
        sm=SMOTE(k_neighbors=1,n_jobs=-1)
        svc=SVC(kernel='rbf',probability=True)
        rfc=RandomForestClassifier()
        #mb=MultinomialNB()
        xgc=XGBClassifier()
        pipe=make_pipeline(tcv,tfv,sm,xgc)
        #pipe=make_pipeline(tcv,tfv,mb)
        pipe.fit(X=X_train,y=y_train)
        y_predict=pipe.predict(X_test)
        print(classification_report(y_test,y_predict))
        print("Accuracy",accuracy_score(y_test,y_predict))
        accuracy=accuracy+round(accuracy_score(y_test,y_predict)*100,2)
    return round(accuracy/len(stream),2)

def estevaluation(dataframe):
    print("evaluation")
    try:
        dataframe=missing_values_treatment(dataframe)
        dataframe[['Seggregation','Application']]=pd.DataFrame(dataframe[['Title','Module']].apply(seggregation,axis=1))
        dataframe['Complexity']=pd.DataFrame(dataframe[['Severity','Estimate']].apply(Estimation,axis=1))
    except Exception as e:
        return {"message":"error"} 
    dataframe=current_developer(dataframe,current_developers)
    X=dataframe['Title']+' '+dataframe['Application']+' '+dataframe['Seggregation']
    y=dataframe['Complexity']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)
    tcv=CountVectorizer(analyzer=text_process)
    tfv=TfidfTransformer()
    sm=SMOTE(k_neighbors=1,n_jobs=-1)
    svc=SVC(kernel='rbf',probability=True)
    rfc=RandomForestClassifier()
    #mb=MultinomialNB()
    xgc=XGBClassifier()
    pipe=make_pipeline(tcv,tfv,sm,xgc)
    #pipe=make_pipeline(tcv,tfv,mb)
    pipe.fit(X=X_train,y=y_train)
    y_predict=pipe.predict(X_test)
    print(classification_report(y_test,y_predict))
    print("Accuracy",accuracy_score(y_test,y_predict))
    return round(accuracy_score(y_test,y_predict)*100,2)

# def run_model(dataframe,projectid=1):
#     dataframe=missing_values_treatment(dataframe)
#     dataframe[['Seggregation','Application']]=pd.DataFrame(dataframe[['Title','Module']].apply(seggregation,axis=1))
#     dataframe['Complexity']=pd.DataFrame(dataframe[['Severity','Estimate']].apply(Estimation,axis=1))
#     #except Exception as e:
#     #print(e)
#     #return {"message":e} 
#     for i in stream.items():
#         streamdeveloper=get_current_developer_bystream(i[1],projectid)
#         print(i[0]," developers")
#         print(streamdeveloper)
#         current_dataframe=current_developer(dataframe,streamdeveloper)
#         devmodel=devmodelling(current_dataframe)
#         estmodel=estmodelling(current_dataframe)
#         print("Model Generated as pickle file")
#         pickle.dump(devmodel,open('devmodel'+str(i[0])+"_"+str(projectid)+'.pkl', 'wb'))
#         pickle.dump(estmodel,open('estmodel'+str(i[0])+"_"+str(projectid)+'.pkl', 'wb'))
#     #return model
#     return {"message": "Model ran successfull"},200

def run_model(dataframe,projectid=1):
    try:
        dataframe=missing_values_treatment(dataframe)
        dataframe[['Seggregation','Application']]=pd.DataFrame(dataframe[['Title','Module']].apply(seggregation,axis=1))
        dataframe['Complexity']=pd.DataFrame(dataframe[['Severity','Estimate']].apply(Estimation,axis=1))
    except Exception as e:
        print(e)
        return {"message":e} 
    for i in stream.items():
        streamdeveloper=get_current_developer_bystream(i[1],projectid)
        streamtester=get_current_developer_bystream(i[1],projectid,profile=2)
        print("Test stream")
        print(streamtester)
        print(i[0]," developers")
        print(streamdeveloper)
        current_dataframe=current_developer(dataframe,streamdeveloper)
        devmodel=devmodelling(current_dataframe)
        estmodel=estmodelling(current_dataframe)
        current_test_dataframe=current_tester(dataframe,streamtester)
        testmodel=testmodelling(current_test_dataframe)
        print("Model Generated as pickle file")
        pickle.dump(devmodel,open('devmodel'+str(i[0])+"_"+str(projectid)+'.pkl', 'wb'))
        pickle.dump(estmodel,open('estmodel'+str(i[0])+"_"+str(projectid)+'.pkl', 'wb'))
        pickle.dump(testmodel,open('testmodel'+str(i[0])+"_"+str(projectid)+'.pkl', 'wb'))
    #return model
    return {"message": "Model ran successfull"},200

def text_process(title):
    #print("Text Processing")
    title=title.lower()
    title=re.sub(r'[-()\"#/@;:<>{}`+=~|.!?,]',r'',title)
    title=''.join([char for char in title if char not in string.punctuation])
    clean_title=[word for word in title.split() if word not in stopwords.words('english')]
    wordnet_lem=WordNetLemmatizer()
    lemma=[wordnet_lem.lemmatize(word,pos='v') for word in clean_title]
    return lemma

def vectorization(Xtrain,Xtest,feature):
    cv=CountVectorizer(analyzer=text_process)
    cv1=cv.fit(Xtrain[feature])
    X_temp=pd.DataFrame(cv1.transform(Xtrain[feature].values.astype('U')).todense(),columns=cv1.get_feature_names()) 
    X_test1=pd.DataFrame(cv1.transform(Xtest[feature].values.astype('U')).todense(),columns=cv1.get_feature_names())
    return (X_temp,X_test1)

def recommended_developer(lis):  
    global current_developers
    lis=lis[current_developers]
    return lis[lis.values==max(lis.values)].index[0]
    #return bestpipeline.classes_[lis.index(max(lis))]

# def latest_defect():
#     connection_string="Driver={SQL Server};"+"Server=(local);"+"Database=TFS;"+"username=DCTSqlUser;"+"password=orange#5;"+"Trusted_connect=yes;"
#     query="select * from TFSDATA where "

# def model_building(dataframe):
#     X=dataframe[['Title','Module']]
#     y=dataframe['Developer']
#     X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)
#     X_temp1,X_test1=vectorization(X_train,X_test,'Title')
#     X_temp2,X_test2=vectorization(X_train,X_test,'Module') 
#     X_train_sm=pd.concat([X_temp1,X_temp2],axis=1)
#     X_test_sm=pd.concat([X_test1,X_test2],axis=1)  
#     model=MultinomialNB().fit(X_train_sm,y_train)   
#     # final_df=pd.DataFrame(100*(model.predict_proba(X_test_sm).round(4)),columns=model.classes_,index=X_test_sm.index)
#     # df_f=final_df.reset_index()
#     # final_df['Recommended Developer']=final_df.apply(recommended_developer,axis=1)
#     # bestpipeline=Pipeline([('tokenization',CountVectorizer(analyzer=text_process)),
#     # ('tfidf',TfidfTransformer()),
#     # ('clf',SVC(kernel='rbf',probability=True))],verbose=True)#n_estimators=100,max_depth=5,min_samples_split=10,min_samples_leaf=10,criterion='gini'
#     # bestpipeline.fit(X_train,y_train)
#     # pickle_file=open('TFSmodel.pickel','wb')
#     # print(bestpipeline.predict('Coverage Match'))
#     # pickle.dump(bestpipeline,pickle_file)
#     # return bestpipeline
#     return model

if __name__ == "__main__":
    run_model(dataframe)

    
