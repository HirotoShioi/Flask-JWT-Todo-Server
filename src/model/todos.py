from typing import Optional, Any
from db import db
from datetime import datetime


class TodoModel(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(80))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    store = db.relationship("UserModel")

    def __init__(self, todo: str, user_id: int):
        self.todo = todo
        self.user_id = user_id

    def json(self) -> Any:
        return {
            "id": self.id,
            "todo": self.todo,
            "complete": self.completed,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
        }

    @classmethod
    def find_by_user_id(cls, user_id: int) -> Optional[Any]:
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_todo_id(cls, todo_id: int, user_id: int) -> Optional[Any]:
        return cls.query.filter_by(id=todo_id, user_id=user_id).first()

    @classmethod
    def toggle_todo(cls, todo_id: int, user_id: int) -> Optional[Any]:
        todo = cls.query.filter_by(id=todo_id, user_id=user_id).first()
        if todo:
            todo.completed = not todo.completed
            db.session.commit()
            return todo
        else:
            return None

    @classmethod
    def delete_todo(cls, todo_id: int, user_id: int) -> Optional[Any]:
        todo = cls.query.filter_by(id=todo_id, user_id=user_id).first()
        if todo:
            todo.delete_from_db()
            return todo
        else:
            return None

    def add_todo(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
