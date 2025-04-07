from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import secrets


def login(username, password):
    try:
        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()
        db.session.commit()
        if not user:
            raise Exception("User doesn't exist")
        else:
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                session["csrf_token"] = secrets.token_hex(16)
                return True
            else:
                raise Exception("Wrong password")
    except Exception as error:
        raise error


def logout():
    del session["user_id"]
    del session["csrf_token"]


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
        return True

    except Exception as error:
        raise error


def get_id():
    return session.get("user_id", 0)


def get_name(id):
    sql = text("SELECT username FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    row = result.fetchone()
    db.session.commit()
    if row:
        return row.username
    return None


def set_name(id, new_name):
    try:
        sql = text("UPDATE users SET username=:new_name WHERE id=:id")
        db.session.execute(sql, {"new_name": new_name, "id": id})
        db.session.commit()
        return True
    except Exception as error:
        raise error


def get_password(id):
    sql = text("SELECT password FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    row = result.fetchone()
    db.session.commit()
    if row:
        return row.password
    return None


def set_password(id, new_password):
    try:
        hash_value = generate_password_hash(new_password)
        sql = text("UPDATE users SET password=:hash_value WHERE id=:id")
        db.session.execute(sql, {"hash_value": hash_value, "id": id})
        db.session.commit()
        return True
    except Exception as error:
        raise error


def user_exists(username):
    sql = text("SELECT username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    db.session.commit()
    if user:
        return True
    return False


def set_profile_picture(data):
    try:
        sql = text("DELETE FROM images WHERE user_id=:user_id")
        db.session.execute(sql, {"user_id": get_id()})
        db.session.commit()
        sql = text("INSERT INTO images (user_id,data) VALUES (:user_id,:data)")
        db.session.execute(sql, {"user_id": get_id(), "data": data})
        db.session.commit()
    except Exception as error:
        raise error


def get_profile_picture(id):
    try:
        sql = text("SELECT data FROM images WHERE user_id=:id")
        result = db.session.execute(sql, {"id": id})
        data = result.fetchone()
        db.session.commit()
        if data is None:
            raise Exception("Image doesn't exist")
        else:
            return data[0]
    except Exception as error:
        raise error
