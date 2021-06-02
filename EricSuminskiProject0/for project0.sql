DROP TABLE customer, account;

CREATE TABLE customer(
	customer_id serial PRIMARY KEY,
	customer_first_name varchar(50),
	customer_last_name varchar(50)
);

CREATE TABLE account(
	account_id serial PRIMARY KEY,
	account_type varchar(50),
	account_value float,
	client_id int,
	CONSTRAINT fk_client_id FOREIGN KEY (client_id) REFERENCES customer(customer_id) ON DELETE cascade
);

--------------------------------------------------------------------------------------

DROP TABLE customer_t, account_t;

CREATE TABLE customer_t(
	customer_id serial PRIMARY KEY,
	customer_first_name varchar(50),
	customer_last_name varchar(50)
);

CREATE TABLE account_t(
	account_id serial PRIMARY KEY,
	account_type varchar(50),
	account_value float,
	client_id int,
	CONSTRAINT fk_client_id FOREIGN KEY (client_id) REFERENCES customer_t(customer_id) ON DELETE cascade
);

INSERT INTO "Project0".customer_t VALUES (DEFAULT, 'test', 'testington');
INSERT INTO "Project0".customer_t VALUES (DEFAULT, 'for', 'account_t testing');
---------------------------------------------------------------------------------------

INSERT INTO "Project0".customer_t VALUES (DEFAULT, 'test', 'testington');
INSERT INTO "Project0".customer_t VALUES (DEFAULT, 'for', 'account_t testing');

SELECT * FROM customer_t WHERE customer_id = 2;

SELECT * FROM "Project0".customer_t;

UPDATE "Project0".customer_t SET customer_first_name = 'brand new', customer_last_name = 'me!' WHERE customer_id = 2

DELETE FROM "Project0".customer_t WHERE customer_id = 2
---------------------------------------------------------------------------

INSERT INTO "Project0".account_t VALUES (DEFAULT, 'checking', '1000', 1)

SELECT * FROM "Project0".account_t WHERE account_id = 1

