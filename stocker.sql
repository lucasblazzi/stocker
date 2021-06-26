CREATE SCHEMA IF NOT EXISTS stocker

CREATE TYPE stocker.profile AS ENUM (
    'admin',
    'advisor',
);

CREATE TABLE IF NOT EXISTS stocker.user(
    cpf INT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
	username VARCHAR(20) UNIQUE NOT NULL,
	password VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL,
	profile stocker.profile NOT NULL,
    cvm_license INT
);

CREATE TABLE IF NOT EXISTS stocker.company (
    symbol VARCHAR(5) NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    exchange VARCHAR(40) NOT NULL,
    industry VARCHAR(130) NOT NULL,
	website VARCHAR(40),
	description TEXT,
	CEO VARCHAR(30) NOT NULL,
    sector VARCHAR(50) NOT NULL,
    employees INT,
    state VARCHAR(20),
	city VARCHAR(20),
	country VARCHAR(20),
	logo VARCHAR(80)
);

CREATE TABLE IF NOT EXISTS stocker.price(
	symbol VARCHAR(5) NOT NULL,
    date DATE NOT NULL,
    close REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    open REAL NOT NULL,
	volume INT NOT NULL,
    FOREIGN KEY(symbol) REFERENCES stocker.company(symbol) ON DELETE CASCADE,
	PRIMARY KEY (symbol, date)
);

CREATE TABLE IF NOT EXISTS stocker.news(
	id SERIAL PRIMARY KEY,
	symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    title VARCHAR(200) NOT NULL,
    source VARCHAR(100),
    url VARCHAR(100),
	description TEXT,
	image VARCHAR(100),
    FOREIGN KEY(symbol) REFERENCES stocker.company(symbol) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS stocker.crypto (
	symbol VARCHAR(15) NOT NULL PRIMARY KEY,
	name VARCHAR(25) NOT NULL,
	currency VARCHAR(5) NOT NULL,
	price REAL NOT NULL,
	price_date DATE NOT NULL
);



CREATE UNIQUE INDEX login_idx ON stocker.user (username, password);

CREATE extension pg_trgm;
CREATE INDEX name_crypto_idx ON stocker.crypto USING gin (name gin_trgm_ops);

CREATE EXTENSION pgcrypto;

CREATE OR REPLACE FUNCTION login(user_input VARCHAR(20), pass_input VARCHAR(20)) RETURNS VARCHAR(20) AS $$
	SELECT u.profile FROM stocker.user u WHERE u.username = user_input AND u.password = crypt(pass_input, password)
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION get_prices(symbol_input VARCHAR(200), period_input VARCHAR(10)) RETURNS SETOF stocker.price AS $$
	BEGIN
		IF period_input = '1m' THEN
			RETURN QUERY
			SELECT * FROM stocker.price p WHERE p.symbol = ANY(string_to_array(symbol_input, ' ')) and p.date BETWEEN (CURRENT_DATE - interval '1 month') AND CURRENT_DATE;
		END IF;
		IF period_input = '6m' THEN
			RETURN QUERY
			SELECT * FROM stocker.price p WHERE p.symbol = ANY(string_to_array(symbol_input, ' ')) and p.date BETWEEN (CURRENT_DATE - interval '6 month') AND CURRENT_DATE;
		END IF;
		IF period_input = '1y' THEN
			RETURN QUERY
			SELECT * FROM stocker.price p WHERE p.symbol = ANY(string_to_array(symbol_input, ' ')) and p.date BETWEEN (CURRENT_DATE - interval '1 year') AND CURRENT_DATE;
		END IF;
		IF period_input = '2y' THEN
			RETURN QUERY
			SELECT * FROM stocker.price p WHERE p.symbol = ANY(string_to_array(symbol_input, ' ')) and p.date BETWEEN (CURRENT_DATE - interval '2 year') AND CURRENT_DATE;
		END IF;
		IF period_input = '5y' THEN
			RETURN QUERY
			SELECT * FROM stocker.price p WHERE p.symbol = ANY(string_to_array(symbol_input, ' ')) and p.date BETWEEN (CURRENT_DATE - interval '5 year') AND CURRENT_DATE;
		END IF;
		IF period_input = 'max' THEN
			RETURN QUERY
			SELECT * FROM stocker.price p WHERE p.symbol = ANY(string_to_array(symbol_input, ' '));
		END IF;
	END;
	$$ LANGUAGE 'plpgsql'
