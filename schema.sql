-- schema.sql
-- Database schema for Venmito project

-- People table (core user data)
CREATE TABLE IF NOT EXISTS people (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    devices VARCHAR(255),
    phone VARCHAR(20) UNIQUE,
    dob DATE
);

-- Promotions table
CREATE TABLE IF NOT EXISTS promotions (
    promotion_id BIGINT PRIMARY KEY,
    user_id INTEGER REFERENCES people(user_id),
    promotion VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2),
    responded VARCHAR(3) CHECK (responded IN ('Yes', 'No')),
    promotion_date TIMESTAMP
);

-- Transfers table
CREATE TABLE IF NOT EXISTS transfers (
    transfer_id BIGINT PRIMARY KEY,
    sender_id INTEGER REFERENCES people(user_id),
    recipient_id INTEGER REFERENCES people(user_id),
    amount DECIMAL(10, 2) NOT NULL,
    timestamp DATE
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    user_id INTEGER REFERENCES people(user_id),
    item VARCHAR(100) NOT NULL,
    store VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    price_per_item DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP
);

-- User-level transaction summaries
CREATE TABLE IF NOT EXISTS user_transactions (
    user_id INTEGER PRIMARY KEY REFERENCES people(user_id),
    total_spent DECIMAL(12, 2) DEFAULT 0,
    transaction_count INTEGER DEFAULT 0,
    favorite_store VARCHAR(100),
    favorite_item VARCHAR(100)
);

-- Item-level summaries
CREATE TABLE IF NOT EXISTS item_summary (
    item_id SERIAL PRIMARY KEY,
    item VARCHAR(100) UNIQUE NOT NULL,
    total_revenue DECIMAL(12, 2) DEFAULT 0,
    items_sold INTEGER DEFAULT 0,
    transaction_count INTEGER DEFAULT 0,
    average_price DECIMAL(10, 2)
);

-- Store-level summaries
CREATE TABLE IF NOT EXISTS store_summary (
    store_id SERIAL PRIMARY KEY,
    store VARCHAR(100) UNIQUE NOT NULL,
    total_revenue DECIMAL(12, 2) DEFAULT 0,
    items_sold INTEGER DEFAULT 0,
    total_transactions INTEGER DEFAULT 0,
    average_transaction_value DECIMAL(10, 2),
    most_sold_item VARCHAR(100),
    most_profitable_item VARCHAR(100)
);

-- User-level transfer summaries
CREATE TABLE IF NOT EXISTS user_transfers (
    user_id INTEGER PRIMARY KEY REFERENCES people(user_id),
    total_sent DECIMAL(12, 2) DEFAULT 0,
    total_received DECIMAL(12, 2) DEFAULT 0,
    net_transferred DECIMAL(12, 2) DEFAULT 0,
    sent_count INTEGER DEFAULT 0,
    received_count INTEGER DEFAULT 0,
    transfer_count INTEGER DEFAULT 0
);

-- Create indexes for frequently queried columns
CREATE INDEX IF NOT EXISTS idx_transfers_sender ON transfers(sender_id);
CREATE INDEX IF NOT EXISTS idx_transfers_recipient ON transfers(recipient_id);
CREATE INDEX IF NOT EXISTS idx_transactions_user ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_store ON transactions(store);
CREATE INDEX IF NOT EXISTS idx_transactions_item ON transactions(item);
CREATE INDEX IF NOT EXISTS idx_promotions_user ON promotions(user_id);