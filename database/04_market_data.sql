CREATE TABLE market_data (
    id BIGSERIAL PRIMARY KEY,

    company_id BIGINT REFERENCES companies(id),

    trading_date DATE,

    open NUMERIC,

    high NUMERIC,

    low NUMERIC,

    close NUMERIC,

    volume BIGINT,

    rsi NUMERIC,

    macd NUMERIC,

    sma20 NUMERIC,

    sma50 NUMERIC,

    volatility NUMERIC
    UNIQUE(company_id, trading_date)
);