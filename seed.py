import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM listings")
db.execute("DELETE FROM comments")

user_count = 1000
listing_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username, city, joined) VALUES (?, ?, datetime('now'))",
               ["user" + str(i), "Testcity"])
    
for i in range(1, listing_count + 1):
    user_id = random.randint(1, user_count)
    db.execute("""INSERT INTO listings (name, user_id,  date, info)
                  VALUES (?, ?, datetime('now'), ?)""",
               ["listing" + str(i), user_id, "Test info"])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    listing_id = random.randint(1, listing_count)
    db.execute("""INSERT INTO comments (content, user_id, listing_id, sent_date)
                  VALUES (?, ?, ?, datetime('now'))""",
               ["comment" + str(i), user_id, listing_id])

db.commit()
db.close()
