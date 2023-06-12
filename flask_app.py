from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        return {'data' : data}, 200

    def post(self):
        json = request.get_json()
        req_data = pd.DataFrame({
            'name'      : [json['name']],
            'age'       : [json['age']],
            'city'      : [json['city']]
        })
        data = pd.read_csv('users.csv')
        data = pd.concat([data, req_data], ignore_index=True)
        data.to_csv('users.csv', index=False)
        return {'message' : 'Record successfully added.'}, 200

    def delete(self):
        name = request.args['name']
        data = pd.read_csv('users.csv')

        if name in data['name'].values:
            data = data[data['name'] != name]
            data.to_csv('users.csv', index=False)
            return {'message': 'Record successfully deleted.'}, 200
        else:
            return {'message': 'Record not found.'}, 404

class Cities(Resource):
    def get(self):
        data = pd.read_csv('users.csv',usecols=[2])
        data = data.to_dict('records')
        return {'data' : data}, 200

class Name(Resource):
    def get(self,name):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name :
                return {'data' : entry}, 200
        return {'message' : 'No entry found with this name !'}, 404


# Add URL endpoints
api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/<string:name>')


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    app.run()
