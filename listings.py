import db

def create_listing(name, user_id):
    sql = "INSERT INTO listings (name, user_id, date) VALUES (?, ?, datetime('now'))"
    db.execute(sql, [name, user_id])

def get_listing(id):
    sql = """SELECT id, name, date, image IS NOT NULL has_image
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