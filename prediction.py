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
from get_data import store_data
from datetime import date

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



def load_model():
    # with open(r'./TFSmodel.pickle','rb') as pickle_file:
    #     model=pickle.load(pickle_file)
    print("Loading pickle file")
    model = pickle.load(open('model.pkl','rb'))
    return model



def recommendation_list(lis,Num_developer=3):  
    #print("recommendation_list")
    global current_developers
    #print(lis)
    #lis=lis[current_developers]
    lis=lis.sort_values(ascending=False)
    return list(lis[:Num_developer].index.values)
    
def test(a):
    for i in a:
        lis.append(i)
    return lis
    # title,developer,Id=a
    # return [title,developer,Id]
def tested(a):
    title,developer,Id,s=a
    return [title,developer,Id,s]

def prediction(latest_defect):
    #print(latest_defect)
    print("In Prediction")
    #print(len(latest_defect))
    #print(latest_defect)
    #df=pd.DataFrame(latest_defect,index=range(len(latest_defect)))
    df=latest_defect
    X_test=df['Title']
    #print(X_test)
    model=load_model()
    final_df=pd.DataFrame(100*(model.predict_proba(X_test).round(4)),columns=model.classes_,index=X_test.index)
    #final_df['Recommended Developer']=final_df.apply(recommended_developer,axis=1)
    final_df['Developers']=final_df.apply(recommendation_list,axis=1)
    # final_df=pd.DataFrame(model.predict_proba(X_test),columns=model.classes_,index=X_test.index)
    # final_df['Recommended Developer']=final_df.apply(recommended_developer,axis=1)
    final_df['Title']=X_test
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
    final_df['Date']=date.today()
    final_df['Date']=final_df['Date'].apply(lambda x:x.strftime('%Y-%m-%d'))
    #final_df[['Title','Developers','Id']]
    #final_df['Devel']=final_df['Developers'].str
    final_df[['Date','Title','Developer1','Developer2','Developer3','ID','Recommended']].to_csv('data.csv')
    try:
        store_data('RecommendationsData',final_df[['Date','Title','Developer1','Developer2','Developer3','ID','Recommended']])
    except Exception as e:
        return str(e)
    else:
        return "sucess"
    #res=final_df[['Title','Developers','ID']].apply(test,axis=1)
    #print(res)
    #print(res)
    #return list(res)
    #return final_df[['Title','Developers','Id']].to_json()

