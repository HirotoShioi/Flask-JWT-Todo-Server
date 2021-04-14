from flask_restful import Resource, reqparse
from model.users import UserModel
from flask_jwt import jwt_required, current_identity

user_parser = reqparse.RequestParser()
user_parser.add_argument("username", type=str, required=True, help="Username missing")
user_parser.add_argument("password", type=str, required=True, help="Password missing")


class UserRegister(Resource):
    def post(self) -> object:
        data = user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user:
            return {"message": "User already exists"}, 400
        elif len(data["username"]) < 5:
            return {"message": "Username must be 5 characters or longer"}, 400
        elif len(data["password"]) < 6:
            return {"message": "Password must be more than 6 characters long"}, 400
        else:
            user = UserModel(data["username"], data["password"])
            user.save_to_db()
            return {"message": "User created successfully"}, 201


class UserInformation(Resource):
    @jwt_required()
    def get(self) -> object:
        return current_identity.json()
