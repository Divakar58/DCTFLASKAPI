from flask import Flask,request
from flask_restful import Resource,Api
from model import load_data,current_developer
from predict import predict

app=Flask(__name__)
api=Api(app)


class TFS(Resource):
    def get(self,name):
        print(a)
        return {'developer':'dinesh'},200

    def post(self,name):
        try:
            data=request.get_json()#force=True,slient=True
            predict(dict(data))
            ticket_id=data['id']
            ticket_title=data['title']
        except Exception as e:
            return {'error':e.message}

        return {'id':ticket_id,'title':ticket_title}

api.add_resource(TFS,'/<dict:name>')
app.run(port=5555,debug=False)
        

