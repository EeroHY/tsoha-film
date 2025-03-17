CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT, 
    password TEXT
);
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users,
    title TEXT, 
    review TEXT, 
    stars INTEGER
);
CREATE TABLE comments (
    id SERIAL PRIMARY KEY, 
    review_id INTEGER REFERENCES reviews,
    user_id INTEGER REFERENCES users,  
    comment TEXT 
);