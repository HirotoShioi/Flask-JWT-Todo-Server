from flask_restful import Resource, reqparse
from model.users import UserModel
# /register
# Add an user

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username missing')
user_parser.add_argument('password', type=str, required=True, help='Password missing')

class UserRegister(Resource):
    def post(self):
        data = user_parser.parse_args();
        user = UserModel.find_by_username(data['username'])
        if user:
            return {'message': 'User already exists'}
        else:
            user = UserModel(data['username'], data['password'])
            try:
                user.add_user()
            except:
                return {'message': 'Exception raised while inserting an user'}
            return {'message': 'User created successfully'}
        
class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        print(user.username)
        if user and user.password == data['password']:
                return user.json()
        else:
            return {'message': 'User not found check your username and password'}