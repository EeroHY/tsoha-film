from app import app
from flask import render_template, request, redirect, session, flash
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import users, reviews


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            return render_template("error.html", message="Form must be filled")
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", notfound=True)


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if not username or not password1 or not password2:
            return render_template("error.html", message="Form must be filled")
        if password1 != password2:
            return render_template("error.html", message="Passwords are different")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html")


@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html")


@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "GET":
        list = reviews.get_list()
        print(list)
        return render_template("reviews.html", reviews=list)
    if request.method == "POST":
        title = request.form["title"]
        review = request.form["review"]
        stars = request.form["stars"]
        if not title or not text or not stars:
            return render_template("error.html", message="Form must be filled")
        if reviews.add(users.user_id(), title, review, stars):
            return redirect("/review")
        else:
            return render_template("error.html", message="Failed to add review")
