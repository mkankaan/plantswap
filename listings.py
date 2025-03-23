import db

def create_listing(name, user_id):
    sql = "INSERT INTO listings (name, user_id, date) VALUES (?, ?, datetime('now'))"
    db.execute(sql, [name, user_id])