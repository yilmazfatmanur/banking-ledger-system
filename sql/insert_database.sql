INSERT INTO customers (name) VALUES ("Ali");
INSERT INTO customers (name) VALUES ("Ayşe");

INSERT INTO accounts (customer_id , balance) VALUES (1,500);
INSERT INTO accounts (customer_id , balance) VALUES (2,1000);

SELECT * FROM customers;
SELECT * FROM accounts;   