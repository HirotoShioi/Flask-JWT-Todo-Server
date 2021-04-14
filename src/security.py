from typing import Optional, Any
from resources.users import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username: str, password: str) -> Optional[Any]:
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(password.encode("utf-8"), user.password.encode("utf-8")):
        return user
    else:
        return None


def identify(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
