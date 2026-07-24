CREATE TABLE prediction_performance (
    id BIGSERIAL PRIMARY KEY,

    prediction_id BIGINT REFERENCES predictions(id),

    actual_move NUMERIC,

    direction_correct BOOLEAN,

    score_error NUMERIC,

    created_at TIMESTAMP DEFAULT NOW()
);