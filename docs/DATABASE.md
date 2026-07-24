# Database Design

## Companies

- company_id
- ticker
- company_name
- exchange
- sector
- industry
- market_cap
- website
- logo_url

---

## Earnings

- earnings_id
- company_id
- earnings_date
- session
- eps_estimate
- eps_actual
- revenue_estimate
- revenue_actual
- guidance
- beat_miss

---

## Predictions

- prediction_id
- company_id
- prediction_date
- direction
- probability
- confidence
- earningsedge_score
- expected_move
- ai_reasoning
- actual_move
- correct

---

## Technicals

- company_id
- date
- rsi
- macd
- sma20
- sma50
- ema20
- ema50
- volume
- volatility

---

## News

- news_id
- company_id
- headline
- summary
- url
- published_at
- sentiment