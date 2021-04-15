from flask_restful import Resource, reqparse
from model.users import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token, create_refresh_token
from passlib.hash import argon2

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
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        else:
            return {"message": "User not found"}, 404


class UserLogin(Resource):
    def post(self) -> object:
        data = user_parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        # this is what the `authenticate()` function did in security.py
        if user and argon2.verify(data["password"], user.password):
            # identity= is what the identity()
            # function did in security.py—now stored in the JWT
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid Credentials!"}, 401
