# NASDAQ Tech Valuation Screener

A Flask-based API for screening NASDAQ tech stocks by valuation metrics and sentiment scores. This application helps investors identify undervalued opportunities through customizable filters.

See the full [Product Requirements Document](docs/prds/2025-11-nasdaq-tech-valuation-screener.md) for detailed project goals and features.

## Quickstart

### Prerequisites
- Python 3.8 or higher

### Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
python -m src.app
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
Check if the API is running.

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "ok"
}
```

---

### Stock Screener
Filter stocks by valuation metrics and sentiment.

**Endpoint:** `GET /screener`

**Query Parameters:**
- `pe_max` (float, optional): Maximum P/E ratio
- `ps_max` (float, optional): Maximum P/S ratio
- `sentiment_min` (float, optional): Minimum sentiment score (0-100)

**Examples:**

Get all stocks:
```bash
curl http://localhost:5000/screener
```

Filter by P/E ratio:
```bash
curl "http://localhost:5000/screener?pe_max=25"
```

Filter by multiple criteria:
```bash
curl "http://localhost:5000/screener?pe_max=30&ps_max=5&sentiment_min=60"
```

**Response:**
```json
[
  {
    "ticker": "MSFT",
    "name": "Microsoft Corporation",
    "pe_ratio": 28.5,
    "ps_ratio": 4.2,
    "sentiment": 75.3
  },
  ...
]
```

---

### Get Stock by Ticker
Retrieve detailed information for a specific stock.

**Endpoint:** `GET /stocks/<ticker>`

**Example:**
```bash
curl http://localhost:5000/stocks/MSFT
```

**Response:**
```json
{
  "ticker": "MSFT",
  "name": "Microsoft Corporation",
  "pe_ratio": 28.5,
  "ps_ratio": 4.2,
  "sentiment": 75.3
}
```

**Error Response (404):**
```json
{
  "error": "Stock not found: INVALID"
}
```

## Documentation

For more information:
- [PRD Index](docs/prds/README.md) - All product requirement documents
- [Main PRD](docs/prds/2025-11-nasdaq-tech-valuation-screener.md) - Detailed project requirements

## Development Notes

- The API loads stock data on startup from the data module
- All endpoints return JSON responses
- Query parameters are validated with appropriate error messages
- The server runs in debug mode by default on port 5000
