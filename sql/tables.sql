DROP TABLE IF EXISTS ledger;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE accounts(
    account_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    balance REAL DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE transactions (
    transactions_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    type TEXT,
    amount REAL
);

CREATE TABLE ledger(
    ledger_id INTEGER PRIMARY KEY,
    transactions_id INTEGER,
    debit_account INTEGER,
    credit_account INTEGER,
    amount REAL
);
