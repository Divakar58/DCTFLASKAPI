# import pickle
# from model import model_building
# from model import get_current_developer
# import pandas as pd

# list_developers=['Divakar Kareddy','Debidatta Dash','Vibha Jain','Arvind Prajapati',
#                             'Nidhi Bendon','Manas Das','Siddharth Tiwari','Rohan Sawant','Kuntal Boxi' ]

# def load_model():
#     # with open(r'./TFSmodel.pickle','rb') as pickle_file:
#     #     model=pickle.load(pickle_file)
#     model = pickle.load(open('model.pkl','rb'))
#     return model

# def recommended_developer(lis):  
#     global list_developers
#     lis=lis[list_developers]
#     return lis[lis.values==max(lis.values)].index[0]
#     #return bestpipeline.classes_[lis.index(max(lis))]

# def recommendation_list(lis,Num_developer=3):  
#     global list_developers
#     lis=lis[list_developers]
#     lis=lis.sort_values(ascending=False)
#     return lis[:Num_developer].to_json()

# def vectorization(Xtrain,Xtest,feature,mod):
#     cv=CountVectorizer(analyzer=text_process)
#     cv1=cv.fit(Xtrain[feature])
#     X_temp=pd.DataFrame(cv1.transform(Xtrain[feature]).todense(),columns=cv1.get_feature_names()) 
#     X_test1=pd.DataFrame(cv1.transform(Xtest[feature]).todense(),columns=cv1.get_feature_names())
#     return (X_temp,X_test1)

# def predict(latest_defect):
#     df=pd.DataFrame(dict(latest_defect)).T
#     X_test=df['Title']
#     #X_test=vectorization_predict(df,'Title')
#     model=load_model()
#     final_df=pd.DataFrame(100*(model.predict_proba(X_test).round(4)),columns=model.classes_,index=X_test.index)
#     df_f=final_df.reset_index()
#     final_df['Recommended Developer']=final_df.apply(recommended_developer,axis=1)
#     final_df['Recommended Developer List']=final_df.apply(recommendation_list,axis=1)
#     # final_df=pd.DataFrame(model.predict_proba(X_test),columns=model.classes_,index=X_test.index)
#     # final_df['Recommended Developer']=final_df.apply(recommended_developer,axis=1)
#     final_df['Title']=X_test['Title'].values
#     return final_df[['Title','Recommended Developer List']].T.to_json()
