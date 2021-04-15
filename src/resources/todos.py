from flask_restful import Resource, reqparse
from model.todos import TodoModel
from flask_jwt import jwt_required, current_identity

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
    parser.add_argument(
        "todo", type=str, required=False, help="This field is required when adding todo"
    )

    @jwt_required()
    def get(self) -> object:
        user_id = current_identity.id
        todos = TodoModel.find_by_user_id(user_id)
        if todos:
            return {"todos": [todo.json() for todo in todos]}
        else:
            return {"todos": []}

    @jwt_required()
    def post(self) -> object:
        data = Todo.parser.parse_args()
        user_id = current_identity.id
        todo = TodoModel(data["todo"], user_id)

        todo.add_todo()
        return todo.json()


class TodoManager(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("user_id", type=int, required=True, help="User id")

    @jwt_required()
    def get(self, id: int) -> object:
        user_id = current_identity.id
        todo = TodoModel.find_by_todo_id(id, user_id)
        if todo:
            return todo.json()
        else:
            return {"message": "Todo not found"}, 404

    @jwt_required()
    def delete(self, id: int) -> object:
        user_id = current_identity.id
        deleted_todo = TodoModel.delete_todo(id, user_id)
        if deleted_todo:
            return {"message": f"Todo deleted: {deleted_todo.todo}"}, 200
        else:
            return {"message": "Todo not found"}, 404

    @jwt_required()
    def post(self, id: int) -> object:
        user_id = current_identity.id
        todo = TodoModel.toggle_todo(id, user_id)
        if todo:
            return todo.json()
        else:
            return {"message": "Todo not found"}, 404
