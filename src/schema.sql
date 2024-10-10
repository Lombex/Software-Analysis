-- USERS TABLE: Stores the application users (admins, etc.)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role INTEGER NOT NULL CHECK (role IN (1, 2, 3, 4)),  -- 1: super_admin, 2: admin, 3: consultant, 4: user
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    salt BLOB NOT NULL
);

-- MEMBERS TABLE: Stores the details of members in the system
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0 AND age < 150),
    gender TEXT CHECK (gender IN ('Male', 'Female', 'Other')),
    weight REAL CHECK (weight > 0 AND weight < 1000),
    address TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    membership_id TEXT UNIQUE NOT NULL
);

-- LOGS TABLE: Logs activities performed by users in the system
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    activity TEXT NOT NULL,
    additional_info TEXT,
    suspicious TEXT CHECK (suspicious IN ('Yes', 'No')),
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);
