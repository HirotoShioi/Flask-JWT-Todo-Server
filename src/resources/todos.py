from flask_restful import Resource, Api, reqparse
from typing import *
import datetime
from model.todos import TodoModel

todos = []
todo_id = 0

# /todo
# GET = Fetch all todos
# Get JSON with data { "todo" : str }
# POST = Post todo

# /todo/:id
# GET = Get specific todo
# POST = Toggle complete field
# DELETE = Delete todo


class Todo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('todo', type=str, required=False,
                        help="Context of todo")
    parser.add_argument('user_id', type=int, required=True, help='User id')

    def get(self):
        data = Todo.parser.parse_args()
        todos = TodoModel.find_by_user_id(data['user_id'])
        return {'todos': list(map(lambda todo: todo.json(), todos))}

    def post(self):
        data = Todo.parser.parse_args()
        todo = TodoModel(data['todo'], data['user_id'])

        try:
            todo.add_todo()
        except:
            return {'message': "An error occured while adding todo"}

        return todo.json()


class TodoManager(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True, help="User id")

    def get(self, id):
        data = TodoManager.parser.parse_args()
        todo = TodoModel.find_by_todo_id(id, data['user_id'])
        if(todo):
            return todo.json()
        else:
            return {'message': 'Todo not found'}, 404

    def delete(self, id):
        data = TodoManager.parser.parse_args()
        TodoModel.delete_from_db(id, data['user_id'])
        return {'message': 'Todo deleted'}, 201

    def post(self, id):
        data = TodoManager.parser.parse_args()
        todo = TodoModel.toggle_todo(id, data['user_id'])
        if todo:
            return todo.json()
