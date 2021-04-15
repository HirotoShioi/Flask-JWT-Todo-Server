from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from resources.todos import Todo, TodoManager
from resources.users import UserRegister, UserInformation
from flask_jwt import JWT
from db import db
from security import authenticate, identify

app = Flask(__name__)

# Configurations BEGIN
app.config["JWT_SECRET_KEY"] = "SECRET_KEY"
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=3600)
app.config["JWT_AUTH_URL_RULE"] = "/login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# Configuration END

api = Api(app)

jwt = JWT(app, authenticate, identify)


@app.route("/")  # type: ignore
def hello() -> object:
    return jsonify({"message": "Hello World"})


api.add_resource(Todo, "/todo")
api.add_resource(TodoManager, "/todo/<int:id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserInformation, "/me")


@app.before_first_request
def create_tables() -> None:
    db.create_all()


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
