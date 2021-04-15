from datetime import timedelta
from typing import Any
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


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback() -> object:
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(
    error: Any,
) -> object:
    # we have to keep the argument here, since it's passed in by the caller internally
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error: Any) -> object:
    return (
        jsonify(
            {
                "message": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback() -> object:
    return (
        jsonify(
            {"message": "The token is not fresh.", "error": "fresh_token_required"}
        ),
        401,
    )


api.add_resource(Todo, "/todo")
api.add_resource(TodoManager, "/todo/<int:todo_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserInformation, "/me")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=False)
