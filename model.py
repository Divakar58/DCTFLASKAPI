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
from imblearn.pipeline import make_pipeline
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
#from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
import xgboost
import re
import pickle
#from prediction import modelling
from get_data import dataframe,get_current_developers
from sklearn.metrics import classification_report,accuracy_score


# list_developers=['Divakar Kareddy','Debidatta Dash','Vibha Jain','Arvind Prajapati',
#                             'Nidhi Bendon','Manas Das','Siddharth Tiwari','Rohan Sawant','Kuntal Boxi' ]
#current_developers=['Divakar Kareddy','Debidatta Dash','Vibha Jain','Arvind Prajapati',
                           # 'Nidhi Bendon','Manas Das','Siddharth Tiwari','Rohan Sawant','Kuntal Boxi' ]
current_developers=get_current_developers()
#print("current developers",current_developers)
Num_developer=3


def load_data(file):
    if re.search('/.xlsx$',flags=re.IGNORECASE):
        return pd.read_excel(file)
    elif re.search('/.csv$',flags=re.IGNORECASE):
        return pd.read_csv(file)
    else:
        return "invalid file format send in csv or xlsx format"

def missing_values_treatment(dataframe):
    dataframe['Developer'][dataframe['Developer'].isna()]='No Developer'
    return dataframe

def get_current_developer():
    return current_developer

def current_developer(dataframe,current_developers):
    return dataframe[dataframe['Developer'].isin(current_developers)]
    #return dataframe.head(500)

# def seggregation(a):
#     x,y=a
#     if(y is not None and x is not None):
#         if 'policy' in y.lower():
#             if 'transact' in x.lower():
#                 return pd.Series(['TransACT','Policy'],index=['Seggregation','Application'])
#             elif 'applicant' in x.lower():
#                 return pd.Series(['Account','Policy'],index=['Seggregation','Application'])
#             elif 'skins' in x.lower() or 'align' in x.lower() or 'javascript' in x.lower() or 'ajax' in x.lower():
#                 return pd.Series(['Skins','Policy'],index=['Seggregation','Application'])
#             elif 'premium' in x.lower() or 'pric' in x.lower():
#                 return pd.Series(['Rating','Policy'],index=['Seggregation','Application'])
#             elif 'privilege' in x.lower() or 'useradmin' in x.lower() or 'roles' in x.lower() or 'entity' in x.lower():
#                 return pd.Series(['UserAdmin','Policy'],index=['Seggregation','Application'])
#             elif 'risk' in x.lower():
#                 return pd.Series(['Risk','Policy'],index=['Seggregation','Application'])
#             elif 'form' in x.lower() or 'doc' in x.lower():
#                 return pd.Series(['Forms','Policy'],index=['Seggregation','Application'])
#             elif 'search' in x.lower():
#                 return pd.Series(['Search','Policy'],index=['Seggregation','Application'])
#             elif 'party' in y.lower() or 'ofac' in y.lower() or 'geo' in y.lower():
#                 return pd.Series(['Party','Policy'],index=['Seggregation','Application'])
#             else:
#                 return pd.Series(['PolicyOther','Policy'],index=['Seggregation','Application'])
#         elif 'billing' in y.lower():
#             if 'invoice' in x.lower():
#                 return pd.Series(['Invoice','Billing'],index=['Seggregation','Application'])
#             elif 'disbursement' in x.lower():
#                 return pd.Series(['Disbursement','Billing'],index=['Seggregation','Application'])
#             elif 'payment' in x.lower():
#                 return pd.Series(['Payment','Billing'],index=['Seggregation','Application'])
#             elif 'schedule' in x.lower():
#                 return pd.Series(['ScheduleActivity','Billing'],index=['Seggregation','Application'])
#             elif 'party' in y.lower() or 'ofac' in y.lower() or 'geo' in y.lower():
#                 return pd.Series(['Party','Billing'],index=['Seggregation','Application'])
#             else:
#                 return pd.Series(['BillingOther','Billing'],index=['Seggregation','Application'])
#         elif 'claims' in y.lower():
#             if 'party' in x.lower() or 'ofac' in x.lower() or 'geo' in x.lower():
#                 return pd.Series(['Party','Claims'],index=['Seggregation','Application'])
#             elif 'coverage' in x.lower():
#                 return pd.Series(['CoverageMatch','Claims'],index=['Seggregation','Application'])
#             elif 'attach' in x.lower():
#                 return pd.Series(['AttachPolicy','Claims'],index=['Seggregation','Application'])
#             else:
#                 return pd.Series(['ClaimsOther','Claims'],index=['Seggregation','Application'])
#         else:
#             return pd.Series(['Other','Other'],index=['Seggregation','Application'])
#     else:
#         return pd.Series(['NULL','NULL'],index=['Seggregation','Application'])

def modelling(dataframe):
    print("modelling")
    X=dataframe['Title']
    y=dataframe['Developer']
    #X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0,random_state=42)
    tcv=CountVectorizer(analyzer=text_process)
    tfv=TfidfTransformer()
    sm=SMOTE(k_neighbors=1,n_jobs=-1)#k_neighbors=3,
    svc=SVC(kernel='rbf',probability=True)
    mb=MultinomialNB()
    rfc=RandomForestClassifier()
    xgb=xgboost()
    pipe=make_pipeline(tcv,tfv,sm,xgb)
    #pipe=make_pipeline(tcv,tfv,mb)
    #pipe.fit(X=X_train,y=y_train)
    pipe.fit(X,y)
    return pipe

def evaluation(dataframe):
    print("evaluation")
    try:
        dataframe=missing_values_treatment(dataframe)
    except Exception as e:
        return {"message":"error"} 
    dataframe=current_developer(dataframe,current_developers)
    X=dataframe['Title']
    y=dataframe['Developer']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)
    tcv=CountVectorizer(analyzer=text_process)
    tfv=TfidfTransformer()
    sm=SMOTE(k_neighbors=1,n_jobs=-1)
    svc=SVC(kernel='rbf',probability=True)
    rfc=RandomForestClassifier()
    #mb=MultinomialNB()
    pipe=make_pipeline(tcv,tfv,sm,rfc)
    #pipe=make_pipeline(tcv,tfv,mb)
    pipe.fit(X=X_train,y=y_train)
    y_predict=pipe.predict(X_test)
    print(classification_report(y_test,y_predict))
    print("Accuracy",accuracy_score(y_test,y_predict))
    return accuracy_score(y_test,y_predict)


def run_model(dataframe):
    try:
        dataframe=missing_values_treatment(dataframe)
    except Exception as e:
        return {"message":e} 
    current_dataframe=current_developer(dataframe,current_developers)
    model=modelling(current_dataframe)
    # print("Model Generated as pickle file")
    pickle.dump(model,open('model.pkl', 'wb'))
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

    
