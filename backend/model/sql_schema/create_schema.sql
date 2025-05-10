CREATE TABLE IF NOT EXISTS people (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    telephone TEXT UNIQUE,
    email TEXT UNIQUE,
    dob DATE NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    android BOOLEAN NOT NULL DEFAULT FALSE,
    iphone BOOLEAN NOT NULL DEFAULT FALSE,
    desktop BOOLEAN NOT NULL DEFAULT FALSE
);


CREATE TABLE IF NOT EXISTS PROMOTIONS (
    id SERIAL PRIMARY KEY,
    promotion TEXT NOT NULL,
    responded TEXT NOT NULL,
    promotion_date DATE NOT NULL,
    email TEXT NOT NULL,
    telephone TEXT NOT NULL,
    FOREIGN KEY (email) REFERENCES people(email)
);

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER NOT NULL,
    telephone TEXT,
    store TEXT NOT NULL,
    item_name TEXT NOT NULL,
    total_price NUMERIC NOT NULL,
    price_per_item NUMERIC NOT NULL,
    quantity INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (telephone) REFERENCES people(telephone)
);

CREATE TABLE IF NOT EXISTS transfers (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    amount NUMERIC NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES people(id),
    FOREIGN KEY (recipient_id) REFERENCES people(id)
);