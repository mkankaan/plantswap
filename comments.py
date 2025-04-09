import db

def create_comment(user_id, listing_id, content):
    sql = "INSERT INTO comments (content, user_id, listing_id, sent_date) VALUES (?, ?, ?, datetime('now'))"
    db.execute(sql, [content, user_id, listing_id])

def fetch_by_listing(listing_id):
    sql = """SELECT c.content, c.user_id, c.sent_date, c.edited_date, c.status comment_status, u.username, u.status user_status, u.image IS NOT NULL has_image, c.edited_date IS NOT NULL edited
             FROM comments c, users u
             WHERE u.id = c.user_id AND
             c.listing_id = ?"""
    return db.query(sql, [listing_id])