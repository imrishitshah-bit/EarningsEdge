CREATE TABLE companies (
    id BIGSERIAL PRIMARY KEY,

    ticker VARCHAR(10) UNIQUE NOT NULL,
    company_name TEXT NOT NULL,

    exchange VARCHAR(20),
    sector TEXT,
    industry TEXT,

    market_cap BIGINT,

    website TEXT,
    logo_url TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);