import db

def create_listing(name, user_id, info, classes):
    sql = "INSERT INTO listings (name, user_id, views, date, info) VALUES (?, ?, -1, datetime('now'), ?)"
    db.execute(sql, [name, user_id, info])

    sql = "INSERT INTO listing_classes (listing_id, option_title, option_value) VALUES (?, ?, ?)"
    listing_id = db.last_insert_id()

    for option_title, option_value in classes:
        print("listing:", name, "add class:", option_title, "value:", option_value)
        db.execute(sql, [listing_id, option_title, option_value])
    
def get_listing(id):
    sql = """SELECT l.id, l.name, l.date, l.user_id, u.username, l.views, l.image_id IS NOT NULL has_image, l.image_id, l.info
             FROM listings l, users u
             WHERE l.user_id = u.id
             AND l.id = ?"""
    result = db.query(sql, [id])
    return result[0] if result else None

def get_listing_classes(listing_id):
    sql = "SELECT option_title, option_value FROM classes WHERE listing_id = ?"
    return db.query(sql, [listing_id])

def get_listings_by_page(page, page_size):
    sql = """SELECT l.id listing_id,
                    l.name,
                    l.date,
                    l.image_id IS NOT NULL has_image,
                    u.username,
                    u.id user_id,
                    u.city
             FROM listings l, users u
             WHERE u.id = l.user_id
             ORDER BY l.date DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size*(page-1)
    return db.query(sql, [limit, offset])

def listing_count():
    sql = "SELECT COUNT(*) FROM listings"
    return db.query(sql)[0][0]

def update_image(listing_id, image_id):
    sql = "UPDATE listings SET image_id = ? WHERE id = ?"
    db.execute(sql, [image_id, listing_id])

def remove_image(listing_id):
    sql = "UPDATE listings SET image_id = NULL WHERE id = ?"
    db.execute(sql, [listing_id])

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

def update_listing(listing_id, name, info, classes):
    sql = "UPDATE listings SET (name, info) = (?, ?) WHERE id = ?"
    db.execute(sql, [name, info, listing_id])

    delete_classes(listing_id)

    sql = "INSERT INTO listing_classes (listing_id, option_title, option_value) VALUES (?, ?, ?)"

    for option_title, option_value in classes:
        db.execute(sql, [listing_id, option_title, option_value])

def remove_listing(listing_id):
    delete_classes(listing_id)

    sql = "DELETE FROM listings WHERE id = ?"
    db.execute(sql, [listing_id])

def search(query, city):
    sql = """SELECT l.id listing_id,
                    l.name,
                    l.date,
                    l.image_id IS NOT NULL has_image,
                    u.username,
                    u.id user_id,
                    u.city
             FROM listings l, users u
             WHERE u.id = l.user_id AND
             l.name LIKE ? AND
                   u.city LIKE ?
             ORDER BY l.date DESC"""
    return db.query(sql, ["%" + query + "%", "%" + city + "%"])

def get_all_classes():
    sql = "SELECT option_title, option_value FROM classes"
    class_info = db.query(sql)
    classes = {}

    for class_title, class_option in class_info:
        if class_title in classes:
            classes[class_title].append(class_option)
        else:
            classes[class_title] = [class_option]

    return classes

def get_classes(listing_id):
    sql = "SELECT option_title, option_value FROM listing_classes WHERE listing_id = ?"
    return db.query(sql, [listing_id])

def delete_classes(listing_id):
    sql = "DELETE FROM listing_classes WHERE listing_id = ?"
    db.execute(sql, [listing_id])

