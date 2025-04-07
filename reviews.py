from db import db
from sqlalchemy.sql import text
from datetime import datetime
import pytz

def add(user_id, title, review, stars):
    try:
        tz_HE = pytz.timezone('Europe/Helsinki') 
        datetime_HE = datetime.now(tz_HE)
        date = datetime_HE.strftime('%Y-%m-%d %H:%M:%S')
        sql = text(
            "INSERT INTO reviews (user_id, title, review, stars, date) VALUES (:user_id, :title, :review, :stars, :date)"
        )
        db.session.execute(
            sql, {"user_id": user_id, "title": title, "review": review, "stars": stars, "date": date}
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
            "SELECT reviews.id, users.id, users.username, reviews.title, reviews.stars, reviews.review, reviews.date FROM reviews, users "
            "WHERE reviews.user_id=users.id ORDER BY reviews.id DESC"
        )
        result = db.session.execute(sql)
        return result.fetchall()
    except Exception as error:
        raise error
