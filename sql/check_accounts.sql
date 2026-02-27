--tablo yapı kontrolü--
PRAGMA table_info (accounts);


--foregin key  kontrolü--
PRAGMA foreign_key_list (accounts);

--balance default 0 testi--
INSERT INTO customers (name) VALUES ('test user');
INSERT INTO accounts (customer_id) VALUES (3);

SELECT * FROM accounts WHERE customer_id = 3; 

PRAGMA table_info(ledger);