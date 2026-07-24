CREATE TABLE predictions (
    id BIGSERIAL PRIMARY KEY,

    earnings_id BIGINT REFERENCES earnings(id),

    model_version VARCHAR(20)
    DEFAULT 'v1.0',

    direction VARCHAR(8)
    CHECK (direction IN ('Bullish','Bearish')),

    probability NUMERIC,

    confidence NUMERIC,

    earningsedge_score NUMERIC,

    expected_move NUMERIC,

    ai_reasoning TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);