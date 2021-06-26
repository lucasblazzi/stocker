CREATE SCHEMA IF NOT EXISTS stocker

CREATE TYPE stocker.type_invest AS ENUM (
    'Conservative',
    'Moderate',
    'Bold',
    'Aggressive'
);

CREATE TABLE IF NOT EXISTS stocker.client (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    login VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    cpf VARCHAR(16) NOT NULL,
    birth DATE NOT NULL,
    street VARCHAR(50) NOT NULL,
    num INT NOT NULL,
    city VARCHAR(20) NOT NULL,
    zip VARCHAR(9) NOT NULL,
    state CHAR(2) NOT NULL,
    invest_profile stocker.type_invest NOT NULL
);

CREATE TABLE IF NOT EXISTS stocker.contribution(
    symbol INT NOT NULL,
    date DATE NOT NULL,
    quota_value INT NOT NULL,
    qtd INT NOT NULL,
    id_client INT NOT NULL,
    FOREIGN KEY(id_client) REFERENCES stocker.client(id)
);

CREATE TABLE IF NOT EXISTS stocker.advisor(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    login VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    cvm_code VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS stocker.tip(
    invest_profile stocker.type_invest NOT NULL,
    call VARCHAR(50) NOT NULL,
    symbol INT NOT NULL,
    date DATE NOT NULL,
    code INT PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS stocker.company (
    symbol INT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    exchange VARCHAR(50) NOT NULL,
    industry VARCHAR(50) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    zip VARCHAR(9) NOT NULL,
    employess INT NOT NULL,
    description VARCHAR(200) NOT NULL,
    phone VARCHAR(13) NOT NULL,
    country VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL
);

CREATE TABLE IF NOT EXISTS stocker.price(
    close VARCHAR(50) NOT NULL,
    date DATE NOT NULL PRIMARY KEY,
    high VARCHAR(50) NOT NULL,
    low VARCHAR(50) NOT NULL,
    open VARCHAR(50) NOT NULL,
    symbol_company INT NOT NULL,
    FOREIGN KEY(symbol_company) REFERENCES stocker.company(symbol)
);

CREATE TABLE IF NOT EXISTS stocker.sector(
    name VARCHAR(50) NOT NULL,
    performance VARCHAR(50) NOT NULL,
    updateAt DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS stocker.tip_advisor(
    code_tip INT NOT NULL,
    id_advisor INT NOT NULL,
    FOREIGN KEY(code_tip) REFERENCES stocker.tip(code),
    FOREIGN KEY(id_advisor) REFERENCES stocker.advisor(id),
    PRIMARY KEY (code_tip, id_advisor)
)

