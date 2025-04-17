CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    city TEXT,
    joined TEXT,
    image_id INTEGER DEFAULT NULL,
    status INTEGER DEFAULT 1
);

CREATE TABLE listings (
    id INTEGER PRIMARY KEY,
    name TEXT,
    user_id INTEGER,
    date TEXT,
    views INTEGER,
    cutting INTEGER,
    info TEXT,
    image_id INTEGER DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    user_id INTEGER,
    listing_id INTEGER,
    sent_date TEXT,
    edited_date TEXT DEFAULT NULL,
    status INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (listing_id) REFERENCES listings(id)
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    user_id INTEGER, 
    image BLOB,
    FOREIGN KEY (user_id) REFERENCES users(id)
);