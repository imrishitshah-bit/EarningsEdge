CREATE TABLE news (
    id BIGSERIAL PRIMARY KEY,

    company_id BIGINT REFERENCES companies(id),

    headline TEXT,

    summary TEXT,

    article_url TEXT,

    published_at TIMESTAMP,

    sentiment NUMERIC
);