import db

def create_comment(user_id, listing_id, content):
    sql = "INSERT INTO comments (content, user_id, listing_id, sent_date) VALUES (?, ?, ?, datetime('now'))"
    db.execute(sql, [content, user_id, listing_id])