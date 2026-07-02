CREATE TABLE clients (
    client_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender ENUM('Male','Female') NOT NULL,
    date_of_birth DATE NOT NULL,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    annual_income DECIMAL(12,2),
    risk_profile ENUM('Low','Medium','High'),
    account_open_date DATE
);

CREATE TABLE companies (
    company_id INT PRIMARY KEY,
    stock_symbol VARCHAR(20) UNIQUE NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    sector VARCHAR(50),
    market_cap_billion DECIMAL(15,2)
);

CREATE TABLE stock_prices (
    price_id INT PRIMARY KEY,
    company_id INT NOT NULL,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10,2),
    high_price DECIMAL(10,2),
    low_price DECIMAL(10,2),
    close_price DECIMAL(10,2),
    volume BIGINT,

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE trades (

    trade_id BIGINT PRIMARY KEY,

    client_id INT NOT NULL,

    company_id INT NOT NULL,

    trade_datetime DATETIME,

    trade_type ENUM('BUY','SELL'),

    quantity INT,

    price DECIMAL(10,2),

    brokerage_fee DECIMAL(10,2),

    FOREIGN KEY(client_id)
        REFERENCES clients(client_id),

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE portfolio (

    portfolio_id BIGINT PRIMARY KEY,

    client_id INT,

    company_id INT,

    quantity_held INT,

    average_buy_price DECIMAL(10,2),

    current_value DECIMAL(15,2),

    FOREIGN KEY(client_id)
        REFERENCES clients(client_id),

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE market_indices (

    index_id INT PRIMARY KEY,

    index_name VARCHAR(50),

    trade_date DATE,

    open_value DECIMAL(10,2),

    close_value DECIMAL(10,2),

    daily_change DECIMAL(8,2)
);


SHOW DATABASES;