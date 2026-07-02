USE capital_markets;

-- ==========================================
-- 1. Total Clients
-- ==========================================

SELECT COUNT(*) AS total_clients
FROM clients;

-- ==========================================
-- 2. Total Companies
-- ==========================================

SELECT COUNT(*) AS total_companies
FROM companies;

-- ==========================================
-- 3. Total Trades
-- ==========================================

SELECT COUNT(*) AS total_trades
FROM trades;

-- ==========================================
-- 4. Total Trade Value
-- ==========================================

SELECT
ROUND(SUM(trade_value),2) AS total_trade_value
FROM trades;

-- ==========================================
-- 5. Total Brokerage Revenue
-- ==========================================

SELECT
ROUND(SUM(brokerage_fee),2) AS brokerage_revenue
FROM trades;

-- ==========================================
-- 6. Top 10 Clients by Trade Value
-- ==========================================

SELECT
    c.client_id,
    CONCAT(c.first_name,' ',c.last_name) AS client_name,
    ROUND(SUM(t.trade_value),2) AS total_trade_value
FROM clients c
JOIN trades t
ON c.client_id=t.client_id
GROUP BY c.client_id,client_name
ORDER BY total_trade_value DESC
LIMIT 10;

-- ==========================================
-- 7. Trades by Risk Profile
-- ==========================================

SELECT
    risk_profile,
    COUNT(*) AS total_clients
FROM clients
GROUP BY risk_profile;

-- ==========================================
-- 8. Average Trade Value by Risk Profile
-- ==========================================

SELECT
    c.risk_profile,
    ROUND(AVG(t.trade_value),2) AS average_trade_value
FROM clients c
JOIN trades t
ON c.client_id=t.client_id
GROUP BY c.risk_profile;

-- ==========================================
-- 9. Income Bracket Distribution
-- ==========================================

SELECT
    income_bracket,
    COUNT(*) AS clients
FROM clients
GROUP BY income_bracket;

-- ==========================================
-- 10. Highest Income Clients
-- ==========================================

SELECT
client_id,
first_name,
last_name,
annual_income
FROM clients
ORDER BY annual_income DESC
LIMIT 10;