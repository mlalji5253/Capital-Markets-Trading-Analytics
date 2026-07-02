USE capital_markets;

CREATE OR REPLACE VIEW client_trade_summary AS
SELECT
    c.client_id,
    CONCAT(c.first_name,' ',c.last_name) AS client_name,
    COUNT(t.trade_id) AS total_trades,
    SUM(t.trade_value) AS total_trade_value,
    SUM(t.brokerage_fee) AS total_brokerage
FROM clients c
JOIN trades t
ON c.client_id=t.client_id
GROUP BY c.client_id,client_name;