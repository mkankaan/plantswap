import db

def add_image(image, user_id):
    sql = "INSERT INTO images (image, user_id) VALUES (?,?)"
    db.execute(sql, [image, user_id])

def newest_image_from_user(user_id):
    sql = """SELECT id 
             FROM images
             WHERE user_id = ?
             ORDER BY id DESC
             LIMIT 1 """
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def remove_image(image_id):
    sql = "DELETE FROM images WHERE id = ?"
    db.execute(sql, [image_id])