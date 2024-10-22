from db import db
from sqlalchemy.sql import text

def add(user_id, review, stars):
    try: 
        sql = text("INSERT INTO reviews (user_id, review, stars) VALUES (:user_id, :review, :stars)")
        result = db.session.execute(sql, {"user_id":user_id, "review":review, "stars":stars})   
        db.session.commit()
    except:
        print("failed to create review")
        return False
    return True

def remove(review_id):
    return False

def get_list():
    sql = text("SELECT reviews.stars, reviews.review, users.username FROM reviews, users " \
          "WHERE reviews.user_id=users.id ORDER BY reviews.id")
    result = db.session.execute(sql)
    return result.fetchall()

