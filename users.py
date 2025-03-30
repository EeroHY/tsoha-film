from db import db
from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text


def login(username, password):
    try:
        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()
        if not user:
            raise Exception("User doesn't exist")
        else:
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                return True
            else:
                raise Exception("Wrong password")
    except Exception as error:
        print(str(error))
        flash(str(error))
        return False

def logout():
    del session["user_id"]


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        if user_exists(username):
            raise Exception("User already exists")
        sql = text(
            "INSERT INTO users (username, password) VALUES (:username, :password)"
        )
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except Exception as error:
        print(str(error))
        flash(str(error))
        return False
    return login(username, password)


def user_id():
    return session.get("user_id", 0)


def user_name(id):
    sql = text("SELECT username FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    return result


def user_exists(username):
    sql = text("SELECT username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    return result
