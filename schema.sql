CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT, 
    password TEXT
);
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users, 
    review TEXT, 
    stars INTEGER
);
