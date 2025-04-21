import db

def fetch_all():
    sql = """SELECT id, name
             FROM cities
             ORDER BY name"""
    return db.query(sql)