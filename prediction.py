#from sklearn.naive_bayes import MultinomialNB
#from imblearn.over_sampling import SMOTE
#from sklearn.model_selection import train_test_split
#from nltk.stem import wordnet, WordNetLemmatizer
#from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
#from sklearn.pipeline import Pipeline
#from imblearn.pipeline import make_pipeline
import nltk
from nltk.corpus import stopwords
import string
from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
import pickle
from get_data import store_data,getDataFromRecommnedations,get_current_developers
from datetime import date
from utils.utilfunctions import missing_values_treatment,Estimation,seggregation
from model import stream

current_developers=['Divakar Kareddy','Debidatta Dash','Vibha Jain','Arvind Prajapati',
                            'Nidhi Bendon','Manas Das','Siddharth Tiwari','Rohan Sawant','Kuntal Boxi' ]


# def recommended_developer(lis):  
#     print("recommended_developer")
#     global current_developers
#     lis=lis[current_developers]
#     #print(max(lis.values))
#     return lis[lis.values==max(lis.values)].index[0]
#     #return bestpipeline.classes_[lis.index(max(lis))]

# def text_process(title):
#     print("text processing")
#     title=title.lower()
#     title=''.join([char for char in title if char not in string.punctuation])
#     clean_title=[word for word in title.split() if word not in stopwords.words('english')]
#     wordnet_lem=WordNetLemmatizer()
#     lemma=[wordnet_lem.lemmatize(word,pos='v') for word in clean_title]
#     return lemma



def load_model(projectid=1):
    # with open(r'./TFSmodel.pickle','rb') as pickle_file:
    #     model=pickle.load(pickle_file)
    print("Loading pickle file")
    # devmodel = pickle.load(open('devmodel'+str(projectid)+'.pkl','rb'))
    # estmodel = pickle.load(open('estmodel'+str(projectid)+'.pkl','rb'))
    devmodels=[]
    estmodels=[]
    for i in stream.items():
        print("Loading pickle file",str(i[0]),str(projectid))
        devmodels.append(pickle.load(open(str('devmodel'+str(i[0])+"_"+str(projectid)+'.pkl'), 'rb')))
        estmodels.append(pickle.load(open('estmodel'+str(i[0])+"_"+str(projectid)+'.pkl', 'rb')))    
    return devmodels,estmodels



def recommendation_list(lis,Num_developer=3):  
    #print("recommendation_list")
    global current_developers
    #print(lis)
    #lis=lis[current_developers]
    lis=lis.sort_values(ascending=False)
    
    return list(lis[:Num_developer].index.values)
    
def test(a):
    lis=[]
    for i in a:
        lis.append(i)
    return lis
    # title,developer,Id=a
    # return [title,developer,Id]
def tested(a):
    title,developer,Id,s=a
    return [title,developer,Id,s]

def prediction(latest_defect,projectid,store=True):
    #print(latest_defect)
    print("In Prediction")
    #print(len(latest_defect))
    #print(latest_defect)
    #df=pd.DataFrame(latest_defect,index=range(len(latest_defect)))
    df=latest_defect.copy()
    latest_defect['Estimate']=None
    latest_defect=missing_values_treatment(latest_defect)
    
    latest_defect[['Seggregation','Application']]=pd.DataFrame(latest_defect[['Title','Module']].apply(seggregation,axis=1))
    latest_defect['Complexcity']=pd.DataFrame(latest_defect[['Severity','Estimate']].apply(Estimation,axis=1))
    poldf=latest_defect[latest_defect['Stream']=='Policy']
    bildf=latest_defect[latest_defect['Stream']=='Billing']
    clmdf=latest_defect[latest_defect['Stream']=='Claims']
    #currentdev=get_current_developers()
    #print(X_test)
    [devbilmodel,devclmmodel,devpolmodel],[estbilmodel,estclmmodel,estpolmodel]=load_model(projectid)
    print("pickle file Loaded")
    print("prediction using policy model")
    X_test_pol=poldf['Title']+' '+poldf['Application']+' '+poldf['Seggregation']
    final_pol_df=pd.DataFrame(100*(devpolmodel.predict_proba(X_test_pol).round(4)),columns=devpolmodel.classes_,index=X_test_pol.index)
    print("prediction using billing model")
    X_test_bil=bildf['Title']+' '+bildf['Application']+' '+bildf['Seggregation']
    final_bil_df=pd.DataFrame(100*(devbilmodel.predict_proba(X_test_bil).round(4)),columns=devbilmodel.classes_,index=X_test_bil.index)

    print("prediction using claims model")
    X_test_clm=clmdf['Title']+' '+clmdf['Application']+' '+clmdf['Seggregation']
    final_clm_df=pd.DataFrame(100*(devclmmodel.predict_proba(X_test_clm).round(4)),columns=devclmmodel.classes_,index=X_test_clm.index)

    final_df=pd.concat([final_pol_df,final_bil_df,final_clm_df])
    print(final_df.head())
    final_df.fillna(0,inplace=True)
    #final_df['Recommended Developer']=final_df.apply(recommended_developer,axis=1)
    final_df['Developers']=final_df.apply(recommendation_list,axis=1)
    # final_df=pd.DataFrame(model.predict_proba(X_test),columns=model.classes_,index=X_test.index)
    # final_df['Recommended Developer']=final_df.apply(recommended_developer,axis=1)
    complexcity_pol=pd.DataFrame(100*(estpolmodel.predict_proba(X_test_pol).round(4)),columns=estpolmodel.classes_,index=X_test_pol.index)
    complexcity_bil=pd.DataFrame(100*(estbilmodel.predict_proba(X_test_bil).round(4)),columns=estbilmodel.classes_,index=X_test_bil.index)
    complexcity_clm=pd.DataFrame(100*(estclmmodel.predict_proba(X_test_clm).round(4)),columns=estclmmodel.classes_,index=X_test_clm.index)
    complexcity=pd.concat([complexcity_pol,complexcity_bil,complexcity_clm])
    final_df['Estimate']=round((complexcity['Simple']/100)*8+(complexcity['Medium']/100)*16+(complexcity['Complex']/100)*24+(complexcity['Complicated']/100)*32)
    final_df['Title']=latest_defect['Title']
    final_df['ID']=df['ID'].apply(lambda x:int(x))
    #final_df.to_csv('test.csv')
    #print(final_df[['Title','Recommended Developer List']].T.to_json())
    #print(sortCol,sortDir)
    #final_df.sort_values(by=sortCol,ascending=sortDir,inplace=True)
    #print(final_df)
    final_df['Recommended']=final_df['Developers'].apply(lambda x:x[0])
    final_df['Developer1']=final_df['Developers'].apply(lambda x:x[0])
    final_df['Developer2']=final_df['Developers'].apply(lambda x:x[1])
    final_df['Developer3']=final_df['Developers'].apply(lambda x:x[2])
    final_df['LastUpdated']=date.today()
    final_df['CreatedDate']=pd.to_datetime(latest_defect['CreatedDate'])
    print(final_df['LastUpdated'].isna().sum(),"lasy")
    print(final_df['CreatedDate'].isna().sum(),"create")
    final_df['LastUpdated']=final_df['LastUpdated'].apply(lambda x:x.strftime('%Y-%m-%d'))
    final_df['CreatedDate']=final_df['CreatedDate'].apply(lambda x:x.strftime('%Y-%m-%d'))
    #final_df[['Title','Developers','Id']]
    #final_df['Devel']=final_df['Developers'].str
    final_df.reset_index(inplace=True)
    final_df.sort_values(by='index',inplace=True,ascending=True)
    final_df[['index','CreatedDate','Title','Developer1','Developer2','Developer3','ID','Recommended','LastUpdated','Estimate']].to_csv('data.csv')
    df_old=pd.DataFrame({})
    df_old=getDataFromRecommnedations()
    final_data=pd.read_csv('data.csv')
    final_df1=pd.concat([df_old,final_data])
    final_df1.drop_duplicates(inplace=True)
    print(final_df1.head())
    if(store):
        try:
            store_data('RecommendationsData',final_df1[['index','CreatedDate','Title','Developer1','Developer2','Developer3','ID','Recommended','LastUpdated','Estimate']],'replace')
        except Exception as e:
            print("Exception")
            return str(e)
        else:
            return "sucess"
    elif(store==False):
        res=final_df[['Title','Estimate','ID']].apply(test,axis=1)
        print(res)
        return {'results':list(res)}
    else:
        return "fail"
        #print(res)
        #print(res)
        #return list(res)
        #return final_df[['Title','Developers','Id']].to_json()

def estimation(latest_defect,projectid):
    print("In Estimation")
    df=latest_defect.copy()
    latest_defect['Estimate']=None
    latest_defect=missing_values_treatment(latest_defect)
    final_df=latest_defect.copy()
    latest_defect[['Seggregation','Application']]=pd.DataFrame(latest_defect[['Title','Module']].apply(seggregation,axis=1))
    latest_defect['Complexcity']=pd.DataFrame(latest_defect[['Severity','Estimate']].apply(Estimation,axis=1))
    poldf=latest_defect[latest_defect['Stream']=='Policy']
    bildf=latest_defect[latest_defect['Stream']=='Billing']
    clmdf=latest_defect[latest_defect['Stream']=='Claims']
    X_test_pol=poldf['Title']+' '+poldf['Application']+' '+poldf['Seggregation']
    X_test_bil=bildf['Title']+' '+bildf['Application']+' '+bildf['Seggregation']
    X_test_clm=clmdf['Title']+' '+clmdf['Application']+' '+clmdf['Seggregation']
    [devbilmodel,devclmmodel,devpolmodel],[estbilmodel,estclmmodel,estpolmodel]=load_model(projectid)
    print("pickle file Loaded")
    complexcity_pol=pd.DataFrame({})
    complexcity_bil=pd.DataFrame({})
    complexcity_clm=pd.DataFrame({})
    if(len(X_test_pol.index)>0):
        print("Estimating using policy model")
        complexcity_pol=pd.DataFrame(100*(estpolmodel.predict_proba(X_test_pol).round(4)),columns=estpolmodel.classes_,index=X_test_pol.index)
    if(len(X_test_bil.index)>0):
        print("Estimating using Billing model")
        complexcity_bil=pd.DataFrame(100*(estbilmodel.predict_proba(X_test_bil).round(4)),columns=estbilmodel.classes_,index=X_test_bil.index)
    if(len(X_test_clm.index)>0):
        print("Estimating using Claims model")
        complexcity_clm=pd.DataFrame(100*(estclmmodel.predict_proba(X_test_clm).round(4)),columns=estclmmodel.classes_,index=X_test_clm.index)
    complexcity=pd.concat([complexcity_pol,complexcity_bil,complexcity_clm])
    final_df['Estimate']=round((complexcity['Simple']/100)*8+(complexcity['Medium']/100)*16+(complexcity['Complex']/100)*24+(complexcity['Complicated']/100)*32)
    totalhours=int(sum(final_df['Estimate']))
    res=final_df[['Title','Estimate','ID']].apply(test,axis=1)
    return {'results':list(res),'estimatedHours':totalhours}