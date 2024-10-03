CREATE TABLE visitors (id SERIAL PRIMARY KEY, time TIMESTAMP);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE reviews (id SERIAL PRIMARY KEY, username TEXT, review TEXT, stars INT);
