from sklearn.naive_bayes import MultinomialNB
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from nltk.stem import wordnet, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
#from sklearn.pipeline import Pipeline
from imblearn.pipeline import make_pipeline
import nltk
from nltk.corpus import stopwords
import string
from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
import pickle


current_developers=['Divakar Kareddy','Debidatta Dash','Vibha Jain','Arvind Prajapati',
                            'Nidhi Bendon','Manas Das','Siddharth Tiwari','Rohan Sawant','Kuntal Boxi' ]


def recommended_developer(lis):  
    print("recommended_developer")
    global current_developers
    lis=lis[current_developers]
    print(max(lis.values))
    return lis[lis.values==max(lis.values)].index[0]
    #return bestpipeline.classes_[lis.index(max(lis))]

def text_process(title):
    print("text processing")
    title=title.lower()
    title=''.join([char for char in title if char not in string.punctuation])
    clean_title=[word for word in title.split() if word not in stopwords.words('english')]
    wordnet_lem=WordNetLemmatizer()
    lemma=[wordnet_lem.lemmatize(word,pos='v') for word in clean_title]
    return lemma



def load_model():
    # with open(r'./TFSmodel.pickle','rb') as pickle_file:
    #     model=pickle.load(pickle_file)
    print("Loading pickle file")
    model = pickle.load(open('model.pkl','rb'))
    return model



def recommendation_list(lis,Num_developer=3):  
    print("recommendation_list")
    global current_developers
    print(lis)
    #lis=lis[current_developers]
    lis=lis.sort_values(ascending=False)
    return lis[:Num_developer].to_json()

def prediction(latest_defect):
    print("In Prediction")
    print(len(latest_defect))
    print(latest_defect)
    df=pd.DataFrame(latest_defect,index=range(len(latest_defect)//2))
    X_test=df['Title']
    model=load_model()
    final_df=pd.DataFrame(100*(model.predict_proba(X_test).round(4)),columns=model.classes_,index=X_test.index)
    #final_df['Recommended Developer']=final_df.apply(recommended_developer,axis=1)
    final_df['Recommended Developer List']=final_df.apply(recommendation_list,axis=1)
    # final_df=pd.DataFrame(model.predict_proba(X_test),columns=model.classes_,index=X_test.index)
    # final_df['Recommended Developer']=final_df.apply(recommended_developer,axis=1)
    final_df['Title']=X_test
    final_df['ID']=df['ID']
    #final_df.to_csv('test.csv')
    #print(final_df[['Title','Recommended Developer List']].T.to_json())
    return final_df[['Title','Recommended Developer List','ID']].T.to_json()
