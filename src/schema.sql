CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    registration_date TEXT DEFAULT CURRENT_TIMESTAMP
);




CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    age INTEGER,
    gender TEXT,
    weight REAL,
    address TEXT,
    email TEXT,
    phone TEXT,
    registration_date TEXT,
    membership_id TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY,
    date TEXT,
    time TEXT,
    username TEXT,
    activity TEXT,
    additional_info TEXT,
    suspicious TEXT
);
