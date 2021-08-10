from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
import subprocess

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        return {'data' : data}, 200


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('age', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        new_data = pd.DataFrame({
            'name'      : [args['name']],
            'age'       : [args['age']],
            'city'      : [args['city']]
        })

        data = data.append(new_data, ignore_index = True)
        data.to_csv('users.csv', index=False)
        return {'data' : new_data.to_dict('records')}, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        data = data[data['name'] != args['name']]

        data.to_csv('users.csv', index=False)
        return {'message' : 'Record deleted successfully.'}, 200

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
        return {'message' : 'No entry found with this name !'}, 200

class Name(Resource):
    def get(self,name):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name :
                return {'data' : entry}, 200
        return {'message' : 'No entry found with this name !'}, 200

class DatabaseUsers(Resource):

    def get(self):
        
        output = subprocess.getoutput("PGPASSWORD=123123Aa psql -h 192.168.1.80 -p 5432  -U postgres -c '\du'")
        print(output)
        return {'message' : 'Success.'}, 200
    
        
class Database(Resource):

    def get(self):
        
        output = subprocess.getoutput("PGPASSWORD=123123Aa psql -h 192.168.1.80 -p 5432  -U postgres -c '\l'")
        print(output)
        return {'message' : 'Success.'}, 200
        


# Add URL endpoints
api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/<string:name>')
api.add_resource(Database, '/list_db')
api.add_resource(DatabaseUsers, '/list_users')




if __name__ == '__main__':
    app.run()