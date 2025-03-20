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

def create_user(username, password, city):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash, city, joined) VALUES (?, ?, ?, datetime('now'))"
    db.execute(sql, [username, password_hash, city])