from werkzeug.security import check_password_hash, generate_password_hash
import db

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return user_id
        
    return None
    
def check_status(user_id):
    sql = "SELECT status FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] == 1 if result else None
        
def create_user(username, password, city):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash, city, joined) VALUES (?, ?, ?, datetime('now'))"
    db.execute(sql, [username, password_hash, city])

def get_user(user_id):
    sql = """SELECT u.id, u.username, u.city, u.joined, u.image_id IS NOT NULL has_image, u.image_id, u.status
             FROM users u
             WHERE u.id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def update_image(user_id, image_id):
    sql = "UPDATE users SET image_id = ? WHERE id = ?"
    db.execute(sql, [image_id, user_id])

def remove_image(user_id):
    sql = "UPDATE users SET image_id = NULL WHERE id = ?"
    db.execute(sql, [user_id])

def get_image(user_id):
    sql = "SELECT image_id FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def get_listings(user_id):
    sql = "SELECT id, name, date, image_id IS NOT NULL has_image FROM listings WHERE user_id = ? ORDER BY date DESC"
    return db.query(sql, [user_id])

# fetches the newest listing posted by the user
def newest_listing(user_id):
    sql = """SELECT id 
             FROM listings
             WHERE user_id = ?
             ORDER BY id DESC
            LIMIT 1 """
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def delete_account(user_id):
    sql = "UPDATE users SET status = 0 WHERE id = ?"
    db.execute(sql, [user_id])

def update_user(user_id, new_username, new_city):
    sql = "UPDATE users SET (username, city) = (?, ?) WHERE id = ?"
    db.execute(sql, [new_username, new_city, user_id])

def change_password(user_id, new_password):
    new_password_hash = generate_password_hash(new_password)
    sql = "UPDATE users SET password_hash = ? WHERE id = ?"
    db.execute(sql, [new_password_hash, user_id])

