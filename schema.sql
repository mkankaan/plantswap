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
    user_id INTEGER REFERENCES users,
    date TEXT,
    views INTEGER DEFAULT 0,
    info TEXT,
    image_id INTEGER DEFAULT NULL
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    listing_id INTEGER REFERENCES listings,
    sent_date TEXT,
    edited_date TEXT DEFAULT NULL
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users, 
    image BLOB
);

CREATE TABLE cities (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    option_title TEXT,
    option_value TEXT
);

CREATE TABLE listing_classes (
    id INTEGER PRIMARY KEY,
    listing_id INTEGER REFERENCES listings,
    option_title TEXT,
    option_value TEXT
);

CREATE INDEX idx_class_listing_id ON listing_classes (listing_id);
CREATE INDEX idx_comment_listing_id ON comments (listing_id);