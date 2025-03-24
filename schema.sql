CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    city TEXT,
    joined TEXT,
    image BLOB
);

CREATE TABLE listings (
    id INTEGER PRIMARY KEY,
    name TEXT,
    user_id INTEGER,
    date TEXT,
    image BLOB,
    views INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);