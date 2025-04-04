from db import db
from sqlalchemy.sql import text


def add(user_id, review_id, comment):
    try:
        sql = text(
            "INSERT INTO comments (user_id, review_id, comment) VALUES (:user_id, :review_id, :comment)"
        )
        db.session.execute(
            sql, {"user_id": user_id, "review_id": review_id, "comment": comment}
        )
        db.session.commit()
        return True
    except Exception as error:
        raise error


def remove_by_review_id(review_id):
    try:
        sql = text(
            "DELETE FROM comments WHERE comments.review_id=:review_id"
        )
        db.session.execute(
            sql, {"review_id": review_id}
        )
        db.session.commit()
        return True
    except Exception as error:
        raise error

def remove(comment_id):
    try:
        sql = text(
            "DELETE FROM comments WHERE comments.id=:comment_id"
        )
        db.session.execute(
            sql, {"comment_id": comment_id}
        )
        db.session.commit()
        return True
    except Exception as error:
        raise error


def get_list():
    sql = text("SELECT comments.id, comments.user_id, users.username, comments.review_id, comment FROM comments, users WHERE comments.user_id=users.id")
    result = db.session.execute(sql)
    return result.fetchall()
