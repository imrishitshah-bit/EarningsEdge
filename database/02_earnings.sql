CREATE TABLE earnings (
    id BIGSERIAL PRIMARY KEY,

    company_id BIGINT REFERENCES companies(id),

    earnings_date DATE NOT NULL,

    session VARCHAR(3) CHECK (session IN ('BMO', 'AMC')),

    fiscal_quarter VARCHAR(10),

    fiscal_year INT,

    eps_estimate NUMERIC,
    eps_actual NUMERIC,

    revenue_estimate BIGINT,
    revenue_actual BIGINT,

    guidance TEXT,

    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE (company_id, earnings_date)
);