import db

def create_listing(name, user_id, cutting, info):
    sql = "INSERT INTO listings (name, user_id, views, date, cutting, info) VALUES (?, ?, -1, datetime('now'), ?, ?)"
    db.execute(sql, [name, user_id, cutting, info])

def get_listing(id):
    sql = """SELECT id, name, date, user_id, views, image_id IS NOT NULL has_image, image_id, cutting, info
             FROM listings
             WHERE id = ?"""
    result = db.query(sql, [id])
    return result[0] if result else None

def update_image(listing_id, image_id):
    sql = "UPDATE listings SET image_id = ? WHERE id = ?"
    db.execute(sql, [image_id, listing_id])

def get_image_id(listing_id):
    sql = "SELECT image_id FROM listings WHERE id = ?"
    result = db.query(sql, [listing_id])
    return result[0][0] if result else None

def add_view(listing_id):
    sql = "UPDATE listings SET views = (SELECT views FROM listings WHERE id = ?)+1 WHERE id = ?"
    db.execute(sql, [listing_id, listing_id])

def get_user(listing_id):
    sql = "SELECT user_id FROM listings WHERE id = ?"
    result = db.query(sql, [listing_id])
    return result[0][0] if result else None

def update_listing(listing_id, name):
    sql = "UPDATE listings SET name = ? WHERE id = ?"
    db.execute(sql, [name, listing_id])

def remove_listing(listing_id):
    sql = "DELETE FROM listings WHERE id = ?"
    db.execute(sql, [listing_id])

def search_query(query):
    sql = """SELECT l.id listing_id,
                    l.name,
                    l.date,
                    l.cutting,
                    l.image_id IS NOT NULL has_image,
                    u.username,
                    u.city
             FROM listings l, users u
             WHERE u.id = l.user_id AND
                   l.name LIKE ?
             ORDER BY l.date DESC"""
    return db.query(sql, ["%" + query + "%"])

def search_city(city):
    sql = """SELECT l.id listing_id,
                    l.name,
                    l.date,
                    l.cutting,
                    l.image_id IS NOT NULL has_image,
                    u.username,
                    u.city
             FROM listings l, users u
             WHERE u.id = l.user_id AND
                   u.city LIKE ?
             ORDER BY l.date DESC"""
    return db.query(sql, ["%" + city + "%"])

def search_query_city(query, city):
    sql = """SELECT l.id listing_id,
                    l.name,
                    l.date,
                    l.cutting,
                    l.image_id IS NOT NULL has_image,
                    u.username,
                    u.city
             FROM listings l, users u
             WHERE u.id = l.user_id AND
             l.name LIKE ? AND
                   u.city LIKE ?
             ORDER BY l.date DESC"""
    return db.query(sql, ["%" + query + "%", "%" + city + "%"])

def fetch_all():
    sql = """SELECT l.id listing_id,
                    l.name,
                    l.date,
                    l.cutting,
                    l.image_id IS NOT NULL has_image,
                    u.id user_id,
                    u.username,
                    u.city
             FROM listings l, users u
             WHERE u.id = l.user_id
             ORDER BY l.date DESC"""
    return db.query(sql)
