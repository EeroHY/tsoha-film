from db import db
from sqlalchemy.sql import text
from flask import flash


def add(user_id, title, review, stars):
    try:
        sql = text(
            "INSERT INTO reviews (user_id, title, review, stars) VALUES (:user_id, :title, :review, :stars)"
        )
        db.session.execute(
            sql, {"user_id": user_id, "title": title, "review": review, "stars": stars}
        )
        db.session.commit()
    except Exception as error:
        print(str(error))
        flash(str(error))
        return False
    return True


def remove(review_id):
    return False


def get_list():
    sql = text(
        "SELECT reviews.id, users.username, reviews.title, reviews.stars, reviews.review FROM reviews, users "
        "WHERE reviews.user_id=users.id ORDER BY reviews.id"
    )
    result = db.session.execute(sql)
    return result.fetchall()
