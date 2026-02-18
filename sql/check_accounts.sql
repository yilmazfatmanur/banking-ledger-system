--tablo yapı kontrolü--
PRAGMA table_info (accounts);


--foregin key  kontrolü--
PRAGMA foregin_key_list (accounts);

--balance default 0 testi--
INSERT INTO cutomers (name) VALUES ('test user');
INSERT INTO accounts (customer_id) VALUES (3);

SELECT * FROM accounts WHERE customer_id = 3; 