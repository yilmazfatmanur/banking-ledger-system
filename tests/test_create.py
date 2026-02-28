#test
import sqlite3
import os

# veritabanı yolu
db_path = os.path.join("..", "bank.db")
print(f"Veritabanı yolu: {db_path}")

# bağlantı
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.executescript('''
DROP TABLE IF EXISTS ledger;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    balance REAL DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE transactions (
    transactions_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    type TEXT,
    amount REAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ledger (
    ledger_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transactions_id INTEGER,
    debit_account INTEGER,
    credit_account INTEGER,
    amount REAL
);
''')

conn.commit()

# tabloları kontrol 
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Oluşturulan tablolar:")
for table in tables:
    print(f"  - {table[0]}")

# test verisi ekle
cursor.execute("INSERT INTO customers (name) VALUES ('Ahmet Hekim')")
cursor.execute("INSERT INTO customers (name) VALUES ('Ayten Veli')")
cursor.execute("INSERT INTO accounts (customer_id, balance) VALUES (1, 1000)")
cursor.execute("INSERT INTO accounts (customer_id, balance) VALUES (2, 2000)")
cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (1, 'deposit', 100)")
cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (1, 'withdraw', 50)")
cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (2, 'deposit', 500)")
cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (2, 'withdraw', 200)")
cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (2, 'withdraw', 100)")
conn.commit()

# veri kontrol
cursor.execute("SELECT COUNT(*) FROM customers")
print(f"Müşteri sayısı: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM accounts")
print(f"Hesap sayısı: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM transactions")
print(f"İşlem sayısı: {cursor.fetchone()[0]}")

conn.close()
print("\n✅ Veritabanı başarıyla oluşturuldu!")