from db import db
from sqlalchemy.sql import text
from flask import flash


def add(user_id, review_id, comment):
    try:
        sql = text(
            "INSERT INTO comments (user_id, review_id, comment) VALUES (:user_id, :review_id, :comment)"
        )
        db.session.execute(
            sql, {"user_id": user_id, "review_id": review_id, "comment": comment}
        )
        db.session.commit()
    except Exception as error:
        print(str(error))
        flash(str(error))
        return False
    return True


def remove(comment_id):
    return False


def get_list():
    sql = text(
        "SELECT comments.user_id, comments.review_id, comment FROM comments "
    )
    result = db.session.execute(sql)
    return result.fetchall()
