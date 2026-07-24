CREATE TABLE model_factors (
    id BIGSERIAL PRIMARY KEY,

    prediction_id BIGINT REFERENCES predictions(id),

    factor_name TEXT,

    factor_value TEXT,

    factor_weight NUMERIC
);