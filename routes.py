from app import app
from flask import render_template, request, redirect, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        session["notfound"] = username
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            del session["notfound"] 
            session["username"] = username
            return redirect("/")
        else:
            session["notfound"] = username
            return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/newUser")
def new():
    return render_template("newUser.html")

@app.route("/createUser", methods=["POST"])
def create():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")