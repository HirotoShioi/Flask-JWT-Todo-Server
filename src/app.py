from flask import Flask, jsonify
from flask_restful import Api
from resources.todos import Todo, TodoManager
from resources.users import UserLogin, UserRegister
from db import db

app = Flask(__name__)

# Configurations BEGIN
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Configuration END

api = Api(app)

@app.route("/")
def hello():
    return jsonify({'message': "Hello World" })

api.add_resource(Todo, '/todo');
api.add_resource(TodoManager, '/todo/<int:id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

@app.before_first_request
def create_tables():
    db.create_all()
    
if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)