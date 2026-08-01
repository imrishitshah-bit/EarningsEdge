# RS Earnings Frontend API Specification

## Overview

RS Earnings uses a FastAPI backend.

The frontend MUST NEVER calculate financial logic.

The backend is the single source of truth for:

- AI Score
- Recommendation
- Grade
- Probability
- Expected Move
- Bull/Base/Bear Cases
- Target Price
- Confidence
- Technical Metrics
- Historical Earnings
- Score Breakdown

The frontend only visualizes backend data.

---

# Base URL

The API base URL must be loaded from

VITE_API_URL

Never hardcode localhost.

Example

https://api.rsearnings.com

---

# Authentication

Currently no authentication.

Future versions will use JWT.

---

# Endpoints

---

## GET /dashboard

Returns dashboard overview.

Example

```json
{
  "companies_covered": 512,
  "reporting_today": 18,
  "reporting_this_week": 71,
  "average_ai_score": 63,
  "highest_rated_company": {
    "ticker": "AMD",
    "company_name": "Advanced Micro Devices",
    "ai_score": 87
  }
}
```

Used for:

Dashboard Quick Stats

---

## GET /rankings

Returns all ranked companies.

Example

```json
[
  {
    "ticker":"AMD",
    "company_name":"Advanced Micro Devices",
    "ai_score":87,
    "grade":"A",
    "recommendation":"Buy",
    "confidence":"High",
    "risk_level":"Medium",
    "expected_move":8.2,
    "earnings_date":"2026-08-04"
  }
]
```

Used for

Top Opportunities

Rankings Page

Search

---

## GET /earnings

Returns upcoming earnings.

Example

```json
[
  {
    "ticker":"AMD",
    "company_name":"Advanced Micro Devices",
    "earnings_date":"2026-08-04",
    "session":"AMC",
    "ai_score":87,
    "grade":"A"
  }
]
```

Used for

Calendar

Upcoming Earnings

Watchlist

---

## GET /companies

Returns company list.

Example

```json
[
  {
    "ticker":"AAPL",
    "company_name":"Apple Inc."
  }
]
```

Used for

Global Search

Autocomplete

---

## GET /scores/{ticker}

Returns complete stock report.

Example

```json
{
  "ticker":"AMD",

  "company_name":"Advanced Micro Devices",

  "ai_score":87,

  "grade":"A",

  "recommendation":"Buy",

  "confidence":"High",

  "risk_level":"Medium",

  "summary":"AMD has strong historical earnings performance with positive momentum heading into earnings.",

  "probability":81,

  "expected_move":8.2,

  "expected_move_confidence":92,

  "bull_case":12.5,

  "base_case":8.2,

  "bear_case":-5.1,

  "target_price":184.25,

  "earnings_date":"2026-08-04",

  "eps_estimate":1.42,

  "revenue_estimate":8120000000,

  "strengths":[
      "...",
      "..."
  ],

  "weaknesses":[
      "...",
      "..."
  ],

  "reasons":[
      "...",
      "..."
  ],

  "technical":{

      "close":170.24,

      "rsi":61.2,

      "macd":2.31,

      "sma20":164.5,

      "sma50":156.3,

      "volatility":0.42,

      "trading_date":"2026-07-31"

  },

  "historical":{

      "quarters_analyzed":8,

      "eps_beats":7,

      "average_surprise":18.4

  },

  "breakdown":{

      "business_quality":67,

      "historical":18,

      "technical":15,

      "momentum":10,

      "risk":9,

      "relative_strength":7,

      "expectation_risk":8,

      "sentiment":5

  }

}
```

Used for

Stock Report

AI Summary

Technical Analysis

Historical Earnings

Expected Move

Target Price

Bull/Base/Bear Cases

Progress Bars

---

# Frontend Rules

Never calculate

AI Score

Probability

Expected Move

Recommendation

Target Price

Bull Case

Base Case

Bear Case

Grades

Risk

Score Breakdown

Display exactly what the backend returns.

---

# Loading States

Every page should have

Skeleton loaders

Retry button

Error state

Empty state

---

# Data Fetching

Use

TanStack Query

Reusable hooks

Examples

useDashboard()

useRankings()

useEarnings()

useCompanies()

useScore(ticker)

---

# Caching

Dashboard

60 seconds

Rankings

60 seconds

Stock Report

5 minutes

Companies

24 hours

---

# Search

Search should use

GET /companies

Autocomplete

Ticker

Company Name

Keyboard Shortcut

Ctrl + K

---

# Philosophy

The backend owns every calculation.

The frontend owns presentation.

Never duplicate business logic.