import db

def create_comment(user_id, listing_id, content):
    sql = """INSERT INTO comments (content, user_id, listing_id, sent_date)
             VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [content, user_id, listing_id])

def get_by_listing(listing_id):
    sql = """SELECT c.id comment_id, c.content, c.user_id, c.sent_date, c.edited_date, u.username, u.status user_status, u.image_id IS NOT NULL user_has_image, c.edited_date IS NOT NULL edited
             FROM comments c, users u
             WHERE u.id = c.user_id AND
             c.listing_id = ?
             ORDER BY c.sent_date DESC"""
    return db.query(sql, [listing_id])

def get_comment(comment_id):
    sql = """SELECT c.id, c.user_id, c.listing_id, c.content, c.sent_date, c.edited_date, u.username, u.image_id IS NOT NULL user_has_image
             FROM comments c, users u
             WHERE c.user_id = u.id AND
             c.id = ?"""
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def update_comment(comment_id, content):
    sql = "UPDATE comments SET (content, edited_date) = (?, datetime('now')) WHERE id = ?"
    db.execute(sql, [content, comment_id])

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def remove_from_listing(listing_id):
    sql = "DELETE FROM comments WHERE listing_id = ?"
    db.execute(sql, [listing_id])