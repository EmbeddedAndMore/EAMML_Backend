from re import U
from ..exceptions import UserAlreadyExists
from ..models.db_models import User


def register(user_json: dict) -> str:
    username = user_json.get("username")
    email = user_json.get("email")
    password = user_json.get("password")

    if not username and not email:
        raise ValueError("User input is wrong")
    if not password:
        raise ValueError("User input is wrong")

    if not username and email:
        username = email

    usr = User(username=username, email=email)
    usr.hash_password(password)
    if usr.check_exists():
        raise UserAlreadyExists
    usr.save()

    return username


def login(user_pass: dict) -> str:
    if "username" not in user_pass or "password" not in user_pass:
        raise ValueError

    user = User(username=user_pass["username"]).get_user()
    if user is not None and user.verify_password(user_pass["password"]):
        return user.username
    else:
        raise ValueError
