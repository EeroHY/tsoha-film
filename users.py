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


def user_exists(username):
    sql = text("SELECT username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    db.session.commit()
    if user:
        return True
    return False

def set_profile_picture(data):
    sql = text("DELETE FROM images WHERE user_id=:user_id")
    db.session.execute(sql, {"user_id":get_id()})
    db.session.commit()
    sql = text("INSERT INTO images (user_id,data) VALUES (:user_id,:data)")
    db.session.execute(sql, {"user_id":get_id(), "data":data})
    db.session.commit()

def get_profile_picture(id):
    sql = text("SELECT data FROM images WHERE user_id=:id")
    result = db.session.execute(sql, {"id":id})
    data = result.fetchone()[0]    
    db.session.commit()
    return data