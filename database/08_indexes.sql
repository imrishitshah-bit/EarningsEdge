CREATE INDEX idx_company_ticker
ON companies(ticker);

CREATE INDEX idx_earnings_date
ON earnings(earnings_date);

CREATE INDEX idx_predictions_earnings
ON predictions(earnings_id);

CREATE INDEX idx_market_company
ON market_data(company_id);

CREATE INDEX idx_news_company
ON news(company_id);