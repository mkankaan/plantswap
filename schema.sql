CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    city TEXT,
    joined TEXT,
    image BLOB,
    status INTEGER DEFAULT 1
);

CREATE TABLE listings (
    id INTEGER PRIMARY KEY,
    name TEXT,
    user_id INTEGER,
    date TEXT,
    image BLOB,
    views INTEGER,
    cutting INTEGER,
    info TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);