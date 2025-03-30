from app import app
from flask import render_template, request, redirect, flash
from sqlalchemy.sql import text
import users, reviews, comments


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    try:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if not username or not password:
                raise Exception("Form must be filled")
            if users.login(username, password):
                return redirect("/")
            else:
                raise Exception("User not found")
    except Exception as error:
        print(str(error))
        flash(str(error))
    return render_template("login.html")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        try:
            username = request.form["username"]
            password1 = request.form["password1"]
            password2 = request.form["password2"]
            if not username or not password1 or not password2:
                raise Exception("Form must be filled")
            if password1 != password2:
                raise Exception("Passwords are different")
            if users.register(username, password1):
                flash("Register successful! You can now login.")
                return redirect("/login")
        except Exception as error:
            print(str(error))
            flash(str(error))
        return render_template("register.html")


@app.route("/profile", methods=["GET"])
def profile():
    print(users.get_name(users.get_id()))
    return render_template("profile.html", username=users.get_name(users.get_id()))


@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "GET":
        try:
            reviews_list = reviews.get_list()
            comments_list = comments.get_list()
            return render_template(
                "reviews.html", reviews=reviews_list, comments=comments_list
            )
        except Exception as error:
            print(str(error))
            flash(str(error))
            return redirect("/")
    if request.method == "POST":
        try:
            title = request.form["title"]
            review = request.form["review"]
            stars = request.form["stars"]
            if not title or not text or not stars:
                raise Exception("Form must be filled")
            if reviews.add(users.get_id(), title, review, stars):
                return redirect("/review")
            else:
                raise Exception("Failed to add review")
        except Exception as error:
            print(str(error))
            flash(str(error))
            return redirect("/review")


@app.route("/comment", methods=["POST"])
def comment():
    try:
        review_id = request.form["review_id"]
        comment = request.form["comment"]
        print(review_id)
        if not comment:
            raise Exception("Form must be filled")
        if comments.add(users.user_id(), review_id, comment):
            return redirect("/review")
        else:
            raise Exception("Failed to add comment")
    except Exception as error:
        print(str(error))
        flash(str(error))
    return redirect("/review")
