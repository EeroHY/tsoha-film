from db import db
from sqlalchemy.sql import text


def add(user_id, title, review, stars):
    try:
        sql = text(
            "INSERT INTO reviews (user_id, title, review, stars) VALUES (:user_id, :title, :review, :stars)"
        )
        db.session.execute(
            sql, {"user_id": user_id, "title": title, "review": review, "stars": stars}
        )
        db.session.commit()
        return True
    except Exception as error:
        raise error


def remove(review_id):
    try:
        sql = text(
            "DELETE FROM reviews WHERE reviews.id=:review_id"
        )
        db.session.execute(
            sql, {"review_id": review_id}
        )
        db.session.commit()
        return True
    except Exception as error:
        raise error


def get_list():
    try:
        sql = text(
            "SELECT reviews.id, users.id, users.username, reviews.title, reviews.stars, reviews.review FROM reviews, users "
            "WHERE reviews.user_id=users.id ORDER BY reviews.id"
        )
        result = db.session.execute(sql)
        return result.fetchall()
    except Exception as error:
        raise error
