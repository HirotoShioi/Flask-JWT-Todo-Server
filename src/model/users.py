from db import db
from typing import Optional, Any


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(16))

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> Optional[Any]:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> Optional[Any]:
        return cls.query.filter_by(id=_id).first()

    def json(self) -> Any:
        return {"user_id": self.id, "username": self.username}
