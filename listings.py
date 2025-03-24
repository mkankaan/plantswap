import db

def create_listing(name, user_id):
    sql = "INSERT INTO listings (name, user_id, views, date) VALUES (?, ?, 0, datetime('now'))"
    db.execute(sql, [name, user_id])

def get_listing(id):
    sql = """SELECT id, name, date, views, image IS NOT NULL has_image
             FROM listings
             WHERE id = ?"""
    result = db.query(sql, [id])
    return result[0] if result else None

def update_image(listing_id, image):
    sql = "UPDATE listings SET image = ? WHERE id = ?"
    db.execute(sql, [image, listing_id])

def get_image(listing_id):
    sql = "SELECT image FROM listings WHERE id = ?"
    result = db.query(sql, [listing_id])
    return result[0][0] if result else None

def add_view(listing_id):
    sql = "UPDATE listings SET views = (SELECT views FROM listings WHERE id = ?)+1 WHERE id = ?"
    db.execute(sql, [listing_id, listing_id])
