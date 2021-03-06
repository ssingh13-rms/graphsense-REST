DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS blacklist_tokens;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE blacklist_tokens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  token TEXT NOT NULL,
  blacklisted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);