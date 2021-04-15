from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from resources.todos import Todo, TodoManager
from resources.users import UserLogin, UserRegister, UserInformation
from db import db
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
    create_access_token,
)

app = Flask(__name__)

# Configurations BEGIN
app.config["JWT_SECRET_KEY"] = "SECRET_KEY"
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=3600)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# Configuration END

api = Api(app)
jwt = JWTManager(app)


@app.route("/")  # type: ignore
def hello() -> object:
    return jsonify({"message": "Welcome to Todo APP"})


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh() -> object:
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


api.add_resource(Todo, "/todo")
api.add_resource(TodoManager, "/todo/<int:todo_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserInformation, "/me")
api.add_resource(UserLogin, "/login")


@app.before_first_request
def create_tables() -> None:
    db.create_all()


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=False)
