CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    city TEXT,
    country TEXT,
    "Android" BOOLEAN,
    "Desktop" BOOLEAN,
    "Iphone" BOOLEAN
);

CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    store TEXT,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS transaction_items (
    id SERIAL PRIMARY KEY,
    transaction_id TEXT REFERENCES transactions(id),
    item_name TEXT,
    price DECIMAL(10,2),
    price_per_item DECIMAL(10,2),
    quantity INT
);

CREATE TABLE IF NOT EXISTS transfers (
    id SERIAL PRIMARY KEY,
    sender_id TEXT REFERENCES clients(id),
    recipient_id TEXT REFERENCES clients(id),
    amount DECIMAL(10,2),
    date DATE
);

CREATE TABLE IF NOT EXISTS promotions (
    id SERIAL PRIMARY KEY,
    client_email TEXT,
    telephone TEXT,
    promotion TEXT,
    responded BOOLEAN DEFAULT FALSE
);