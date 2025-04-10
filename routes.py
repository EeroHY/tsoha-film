from app import app
from flask import render_template, request, redirect, flash, make_response, session
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
                return redirect("/profile")
            else:
                raise Exception("User not found")
    except Exception as error:
        print(str(error))
        flash(str(error))
    return render_template("login.html")


@app.route("/logout")
def logout():
    users.logout()
    flash("Logged out")
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
            if session["csrf_token"] != request.form["csrf_token"]:
                raise PermissionError
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


@app.route("/delete_review", methods=["POST"])
def delete_review():
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            raise PermissionError
        review_id = request.form["review_id"]
        if comments.remove_by_review_id(review_id) and reviews.remove(review_id):
            flash("Deleted review")
            return redirect("/review")
        else:
            raise Exception("Failed to remove review")
    except Exception as error:
        print(str(error))
        flash(str(error))


@app.route("/comment", methods=["POST"])
def comment():
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            raise PermissionError
        review_id = request.form["review_id"]
        comment = request.form["comment"]
        if not comment:
            raise Exception("Form must be filled")
        if comments.add(users.get_id(), review_id, comment):
            return redirect("/review")
        else:
            raise Exception("Failed to add comment")
    except Exception as error:
        print(str(error))
        flash(str(error))
    return redirect("/review")


@app.route("/delete_comment", methods=["POST"])
def delete_comment():
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            raise PermissionError
        comment_id = request.form["comment_id"]
        if comments.remove(comment_id):
            flash("Deleted comment")
            return redirect("/review")
        else:
            raise Exception("Failed to remove comment")
    except Exception as error:
        print(str(error))
        flash(str(error))
        return redirect("/review")


@app.route("/profile", methods=["GET"])
def profile():
    return render_template(
        "profile.html", username=users.get_name(users.get_id()), userid=users.get_id()
    )


@app.route("/change_username", methods=["POST"])
def change_username():
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            raise PermissionError
        new_name = request.form["new_name"]
        if users.set_name(users.get_id(), new_name):
            flash("Name changed successfully!")
            return redirect("/profile")
    except Exception as error:
        print(str(error))
        flash(str(error))
        return redirect("/profile")


@app.route("/change_password", methods=["POST"])
def change_password():
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            raise PermissionError
        username = request.form["username"]
        old_password = request.form["old_password"]
        new_password1 = request.form["new_password1"]
        new_password2 = request.form["new_password2"]
        if not username or not old_password or not new_password1 or not new_password2:
            raise Exception("Form must be filled")
        if new_password1 != new_password2:
            raise Exception("Passwords are different")
        if users.login(username, old_password):    
            if users.set_password(users.get_id(), new_password1):
                flash("Password changed successfully!")
                return redirect("/profile")
        else:
            raise Exception("Wrong password")
    except Exception as error:
        print(str(error))
        flash(str(error))
        return redirect("/profile")


@app.route("/change_picture", methods=["POST"])
def picture():
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            raise PermissionError
        file = request.files["file"]
        name = file.filename
        if not name.endswith(".jpg"):
            raise Exception("Invalid filename")
        data = file.read()
        if len(data) > 1000 * 1024:
            raise Exception("File too big")
        users.set_profile_picture(data)

    except Exception as error:
        print(str(error))
        flash(str(error))
    return redirect("/profile")


@app.route("/image/<int:id>")
def image(id):
    data = users.get_profile_picture(id)
    if data:
        response = make_response(bytes(data))
        response.headers.set("Content-Type", "image/jpeg")
        return response
    else:
        return None
