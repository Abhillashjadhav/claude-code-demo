# NASDAQ Tech Screener MVP - Requirements Specification

## 1. Problem Statement and Goals

### Problem
Investors and analysts need a simple, efficient way to screen NASDAQ-listed technology stocks based on fundamental valuation metrics, growth indicators, and sentiment analysis. Current solutions are often complex, expensive, or lack integration of qualitative signals like management guidance and market sentiment.

### Goals
- Provide a fast, intuitive web-based stock screening tool for NASDAQ tech companies
- Enable multi-criteria filtering using both quantitative (P/E, P/S, market cap, revenue growth) and qualitative (sentiment, management guidance) metrics
- Allow users to save and track stocks of interest via a watchlist
- Support data export for further analysis
- Deliver a clean, responsive UI with dark mode support
- Build an MVP with mock data that can later integrate with real financial APIs

### Success Metrics
- Users can filter 18+ NASDAQ tech stocks by 7+ different criteria
- Filtering operations complete in under 1 second
- Watchlist persists across browser sessions
- Export functionality generates valid CSV files
- Application works on desktop, tablet, and mobile devices
- Dark mode preference is saved and restored

---

## 2. API Endpoints

### Base URL
```
http://localhost:5000/api
```

### 2.1 Health Check
**Endpoint:** `GET /health`

**Description:** Simple health check to verify API is running

**Request:** None

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- 200: API is healthy

---

### 2.2 Get All Stocks
**Endpoint:** `GET /api/stocks`

**Description:** Retrieve all available NASDAQ tech stocks

**Request:** None

**Response:**
```json
[
  {
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "sector": "Consumer Electronics",
    "market_cap": 2800.5,
    "price": 178.25,
    "pe_ratio": 28.5,
    "ps_ratio": 7.2,
    "pb_ratio": 45.3,
    "ev_ebitda": 22.1,
    "revenue_growth": 8.2,
    "earnings_growth": 12.5,
    "sentiment_score": 0.75,
    "sentiment_trend": "up",
    "management_guidance": "positive",
    "volume": 52000000,
    "last_updated": "2025-11-09T10:30:00.000Z"
  }
  // ... more stocks
]
```

**Status Codes:**
- 200: Success

---

### 2.3 Get Stock by Ticker
**Endpoint:** `GET /api/stocks/<ticker>`

**Description:** Retrieve detailed information for a specific stock

**Request Parameters:**
- `ticker` (path parameter): Stock ticker symbol (e.g., "AAPL", "MSFT")

**Response:**
```json
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "sector": "Consumer Electronics",
  "market_cap": 2800.5,
  "price": 178.25,
  "pe_ratio": 28.5,
  "ps_ratio": 7.2,
  "pb_ratio": 45.3,
  "ev_ebitda": 22.1,
  "revenue_growth": 8.2,
  "earnings_growth": 12.5,
  "sentiment_score": 0.75,
  "sentiment_trend": "up",
  "management_guidance": "positive",
  "volume": 52000000,
  "last_updated": "2025-11-09T10:30:00.000Z"
}
```

**Error Response (404):**
```json
{
  "error": "Stock not found"
}
```

**Status Codes:**
- 200: Stock found
- 404: Stock not found

---

### 2.4 Get Sectors
**Endpoint:** `GET /api/sectors`

**Description:** Retrieve list of all unique sectors from available stocks

**Request:** None

**Response:**
```json
[
  "Consumer Electronics",
  "Software",
  "Semiconductors",
  "Internet Services",
  "Social Media",
  "E-Commerce",
  "Cloud Software",
  "FinTech"
]
```

**Status Codes:**
- 200: Success

---

### 2.5 Screen Stocks
**Endpoint:** `POST /api/screen`

**Description:** Filter stocks based on multiple criteria

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "min_market_cap": 100,
  "max_market_cap": 3000,
  "min_pe_ratio": 10,
  "max_pe_ratio": 50,
  "min_ps_ratio": 2,
  "max_ps_ratio": 15,
  "min_revenue_growth": 10,
  "min_sentiment_score": 0.5,
  "sectors": ["Software", "Cloud Software"],
  "management_guidance": "positive"
}
```

**All fields are optional. Only provided filters will be applied.**

**Filter Parameters:**
- `min_market_cap` (float): Minimum market cap in billions
- `max_market_cap` (float): Maximum market cap in billions
- `min_pe_ratio` (float): Minimum P/E ratio
- `max_pe_ratio` (float): Maximum P/E ratio
- `min_ps_ratio` (float): Minimum P/S ratio
- `max_ps_ratio` (float): Maximum P/S ratio
- `min_revenue_growth` (float): Minimum revenue growth percentage
- `min_sentiment_score` (float): Minimum sentiment score (-1 to 1 scale)
- `sectors` (array of strings): List of sectors to include
- `management_guidance` (string): "positive", "neutral", or "negative"

**Response:**
```json
[
  {
    "ticker": "MSFT",
    "name": "Microsoft Corporation",
    // ... full stock object
  }
  // ... more matching stocks
]
```

**Status Codes:**
- 200: Success (returns empty array if no matches)

---

### 2.6 Get Market Statistics
**Endpoint:** `GET /api/stats`

**Description:** Retrieve aggregated statistics across all stocks

**Request:** None

**Response:**
```json
{
  "total_stocks": 18,
  "average_pe": 52.34,
  "average_sentiment": 0.57,
  "guidance_breakdown": {
    "positive": 10,
    "neutral": 6,
    "negative": 2
  }
}
```

**Status Codes:**
- 200: Success

---

## 3. Data Models

### 3.1 Stock Model

**Class:** `Stock` (Python dataclass)

**Fields:**
```python
@dataclass
class Stock:
    ticker: str                    # Stock ticker symbol (e.g., "AAPL")
    name: str                      # Full company name
    sector: str                    # Industry sector
    market_cap: float             # Market capitalization in billions
    price: float                  # Current stock price
    pe_ratio: Optional[float]     # Price-to-Earnings ratio (None if unprofitable)
    ps_ratio: Optional[float]     # Price-to-Sales ratio
    pb_ratio: Optional[float]     # Price-to-Book ratio
    ev_ebitda: Optional[float]    # Enterprise Value to EBITDA ratio
    revenue_growth: float         # Revenue growth percentage (YoY)
    earnings_growth: float        # Earnings growth percentage (YoY)
    sentiment_score: float        # Market sentiment (-1 to 1, where 1 is very positive)
    sentiment_trend: str          # "up", "down", or "stable"
    management_guidance: str      # "positive", "neutral", or "negative"
    volume: int                   # Trading volume
    last_updated: str             # ISO 8601 timestamp
```

**Validation Rules:**
- `ticker`: Must be uppercase, 1-5 characters
- `market_cap`: Must be positive
- `price`: Must be positive
- `pe_ratio`: Can be None for unprofitable companies, otherwise positive
- `ps_ratio`: Can be None, otherwise positive
- `sentiment_score`: Must be between -1 and 1 (inclusive)
- `sentiment_trend`: Must be one of ["up", "down", "stable"]
- `management_guidance`: Must be one of ["positive", "neutral", "negative"]
- `volume`: Must be non-negative integer

**Methods:**
- `to_dict()`: Converts Stock object to dictionary for JSON serialization

---

### 3.2 Screener Filter Model

**Class:** `ScreenerFilter` (Python dataclass)

**Fields:**
```python
@dataclass
class ScreenerFilter:
    min_market_cap: Optional[float] = None
    max_market_cap: Optional[float] = None
    min_pe_ratio: Optional[float] = None
    max_pe_ratio: Optional[float] = None
    min_ps_ratio: Optional[float] = None
    max_ps_ratio: Optional[float] = None
    min_revenue_growth: Optional[float] = None
    min_sentiment_score: Optional[float] = None
    sectors: Optional[List[str]] = None
    management_guidance: Optional[str] = None
```

**Usage:**
Used to validate and process filter criteria from API requests

---

### 3.3 Frontend State Model

**JavaScript State Object:**
```javascript
{
  allStocks: [],           // Array of all stock objects
  filteredStocks: [],      // Array of currently filtered stocks
  watchlist: [],           // Array of ticker symbols in watchlist
  isDarkMode: false        // Boolean for theme preference
}
```

**LocalStorage Schema:**
```javascript
{
  "watchlist": ["AAPL", "MSFT", "NVDA"],  // Array of ticker strings
  "darkMode": "true"                       // String boolean
}
```

---

## 4. Frontend Components

### 4.1 Application Layout

**Main Sections:**
1. Header (app-wide navigation and controls)
2. Stats Dashboard (aggregate market metrics)
3. Screener Layout (filters + results table)
4. Modals (stock details, watchlist)

---

### 4.2 Header Component

**Elements:**
- Logo and title
- Theme toggle button (sun/moon icon)
- Watchlist button with count badge

**Functionality:**
- Toggle between light and dark themes
- Open watchlist modal
- Persist theme preference to localStorage

---

### 4.3 Stats Dashboard Component

**Elements:**
- Total Stocks count
- Average P/E Ratio
- Average Sentiment Score
- Positive Guidance count

**Data Source:** `/api/stats` endpoint

**Update Trigger:** On application initialization

---

### 4.4 Filter Sidebar Component

**Filter Controls:**
1. Market Cap range (min/max inputs)
2. P/E Ratio range (min/max inputs)
3. P/S Ratio range (min/max inputs)
4. Minimum Revenue Growth (single input)
5. Minimum Sentiment Score (single input)
6. Sectors (multi-select checkboxes)
7. Management Guidance (dropdown: All/Positive/Neutral/Negative)

**Action Buttons:**
- Apply Filters (primary button)
- Reset All (text button)

**Functionality:**
- Collect filter values from all inputs
- Send POST request to `/api/screen`
- Clear all filter inputs on reset
- Show all stocks when filters are reset

---

### 4.5 Results Table Component

**Columns:**
1. Ticker (clickable, opens stock details)
2. Company Name
3. Sector
4. Price (formatted with $ and 2 decimals)
5. Market Cap (formatted in billions)
6. P/E Ratio (shows "N/A" if null)
7. P/S Ratio (shows "N/A" if null)
8. Revenue Growth % (colored: green if positive, red if negative)
9. Sentiment (badge with score and trend indicator)
10. Guidance (badge: positive/neutral/negative)
11. Actions (View button + Watchlist star)

**Features:**
- Result count display
- Export to CSV button
- Empty state message when no results
- Loading state while fetching data

**Row Actions:**
- Click ticker or "View" button to open stock details modal
- Click star icon to toggle watchlist status

---

### 4.6 Stock Details Modal

**Header:**
- Company name and ticker
- Close button (X)

**Content Grid (12 items):**
1. Current Price
2. Market Cap
3. P/E Ratio
4. P/S Ratio
5. P/B Ratio
6. EV/EBITDA
7. Revenue Growth %
8. Earnings Growth %
9. Trading Volume
10. Sector
11. Sentiment Score (with trend)
12. Management Guidance

**Footer:**
- Add/Remove from Watchlist button (full width)

**Behavior:**
- Modal opens with stock data populated
- Click outside modal to close
- Updates watchlist status immediately

---

### 4.7 Watchlist Modal

**Header:**
- Title: "My Watchlist"
- Close button (X)

**Content:**
- Empty state: "Your watchlist is empty. Add stocks by clicking the star icon."
- Populated state: List of watchlist items

**Watchlist Item:**
- Ticker and company name
- Current price
- Revenue growth % (colored)
- View button (opens stock details, closes watchlist)
- Remove button (removes from watchlist)

**Behavior:**
- Loads watchlist from localStorage
- Filters allStocks array by watchlist tickers
- Updates immediately when stocks are added/removed

---

### 4.8 CSV Export Feature

**Functionality:**
- Exports currently filtered stocks (not all stocks)
- Generates CSV with headers
- Includes columns: Ticker, Company, Sector, Price, Market Cap, P/E, P/S, Revenue Growth %, Sentiment, Guidance
- Filename format: `nasdaq-tech-screener-YYYY-MM-DD.csv`
- Triggers browser download

**CSV Format:**
```csv
Ticker,Company,Sector,Price,Market Cap (B),P/E,P/S,Revenue Growth %,Sentiment,Guidance
AAPL,Apple Inc.,Consumer Electronics,178.25,2800.5,28.5,7.2,8.2,0.75,positive
```

---

## 5. Edge Cases to Handle

### 5.1 Data Edge Cases

**Null/Missing Values:**
- **Issue:** Some stocks have null `pe_ratio`, `ps_ratio`, `pb_ratio`, or `ev_ebitda` (unprofitable companies)
- **Handling:**
  - Display "N/A" in UI
  - Exclude from average calculations
  - Filter comparisons skip null values (don't match min/max criteria)

**Negative Growth Values:**
- **Issue:** Revenue growth or earnings growth can be negative
- **Handling:**
  - Display with negative sign
  - Color-code red in UI
  - Min revenue growth filter should work with negative values

**Sentiment Score Range:**
- **Issue:** Sentiment scores must be between -1 and 1
- **Handling:**
  - Validate input range in UI (-1 to 1)
  - Backend should validate and reject out-of-range values
  - Classification: >= 0.6 positive, >= 0.3 neutral, < 0.3 negative

---

### 5.2 Filter Edge Cases

**Empty Filter Results:**
- **Issue:** Filter criteria may match zero stocks
- **Handling:** Display message: "No stocks match your filters."

**Invalid Filter Ranges:**
- **Issue:** User enters min > max (e.g., min P/E = 50, max P/E = 20)
- **Handling:**
  - Option 1: Allow (backend returns empty results)
  - Option 2: Show validation error in UI (preferred for better UX)
  - Recommended: Add client-side validation

**No Sectors Selected:**
- **Issue:** User unchecks all sector checkboxes
- **Handling:** Treat as "all sectors" (don't filter by sector)

**Empty POST Body:**
- **Issue:** Client sends POST to /api/screen with empty JSON {}
- **Handling:** Return all stocks (no filters applied)

**Non-existent Ticker:**
- **Issue:** User requests GET /api/stocks/INVALID
- **Handling:** Return 404 with error message

---

### 5.3 UI/UX Edge Cases

**Watchlist Persistence:**
- **Issue:** LocalStorage may be disabled or cleared
- **Handling:**
  - Gracefully handle localStorage errors
  - Default to empty watchlist if parse fails
  - Show message if localStorage is unavailable

**Dark Mode Persistence:**
- **Issue:** Theme preference not loading on page refresh
- **Handling:**
  - Check localStorage on app initialization
  - Apply theme before rendering content (avoid flash)
  - Update icon state to match theme

**API Connection Failure:**
- **Issue:** Backend not running or network error
- **Handling:**
  - Display error message: "Error loading stocks. Please ensure the backend is running."
  - Show loading state during requests
  - Prevent multiple simultaneous filter requests

**Large Watchlist:**
- **Issue:** User adds many stocks to watchlist
- **Handling:**
  - Modal should scroll if content exceeds viewport
  - Consider pagination if > 20 items (future enhancement)

**Modal Accessibility:**
- **Issue:** User opens multiple modals or can't close modal
- **Handling:**
  - Only one modal can be open at a time
  - Close on outside click
  - Close on X button click
  - ESC key to close (future enhancement)

---

### 5.4 Performance Edge Cases

**Rapid Filter Changes:**
- **Issue:** User rapidly clicks "Apply Filters" multiple times
- **Handling:**
  - Disable button while request is in progress (future enhancement)
  - Cancel previous requests (future enhancement)
  - Current: Last request wins

**Large CSV Export:**
- **Issue:** Exporting large filtered result sets
- **Handling:**
  - Current dataset is small (18 stocks max)
  - For production: Add export limit or pagination

---

## 6. Test Cases

### 6.1 Backend API Tests

#### Test Suite: Health Check
```python
def test_health_endpoint():
    """Test that health endpoint returns 200 and correct status"""
    # Arrange
    # Act
    response = client.get('/health')
    # Assert
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}
```

---

#### Test Suite: Get All Stocks
```python
def test_get_all_stocks_returns_200():
    """Test that /api/stocks returns 200 status"""
    response = client.get('/api/stocks')
    assert response.status_code == 200

def test_get_all_stocks_returns_list():
    """Test that /api/stocks returns a list"""
    response = client.get('/api/stocks')
    assert isinstance(response.json, list)

def test_get_all_stocks_count():
    """Test that /api/stocks returns exactly 18 stocks"""
    response = client.get('/api/stocks')
    assert len(response.json) == 18

def test_get_all_stocks_structure():
    """Test that each stock has required fields"""
    response = client.get('/api/stocks')
    stock = response.json[0]
    required_fields = [
        'ticker', 'name', 'sector', 'market_cap', 'price',
        'pe_ratio', 'ps_ratio', 'pb_ratio', 'ev_ebitda',
        'revenue_growth', 'earnings_growth', 'sentiment_score',
        'sentiment_trend', 'management_guidance', 'volume', 'last_updated'
    ]
    for field in required_fields:
        assert field in stock
```

---

#### Test Suite: Get Stock by Ticker
```python
def test_get_stock_by_ticker_success():
    """Test retrieving a valid stock by ticker"""
    response = client.get('/api/stocks/AAPL')
    assert response.status_code == 200
    assert response.json['ticker'] == 'AAPL'
    assert response.json['name'] == 'Apple Inc.'

def test_get_stock_by_ticker_case_insensitive():
    """Test that ticker lookup is case-insensitive"""
    response = client.get('/api/stocks/aapl')
    assert response.status_code == 200
    assert response.json['ticker'] == 'AAPL'

def test_get_stock_by_ticker_not_found():
    """Test 404 for non-existent ticker"""
    response = client.get('/api/stocks/INVALID')
    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == 'Stock not found'
```

---

#### Test Suite: Get Sectors
```python
def test_get_sectors_returns_200():
    """Test that /api/sectors returns 200"""
    response = client.get('/api/sectors')
    assert response.status_code == 200

def test_get_sectors_returns_list():
    """Test that /api/sectors returns a list"""
    response = client.get('/api/sectors')
    assert isinstance(response.json, list)

def test_get_sectors_unique():
    """Test that sectors list contains unique values"""
    response = client.get('/api/sectors')
    sectors = response.json
    assert len(sectors) == len(set(sectors))

def test_get_sectors_contains_expected():
    """Test that sectors list contains known sectors"""
    response = client.get('/api/sectors')
    sectors = response.json
    expected_sectors = ['Software', 'Semiconductors', 'Consumer Electronics']
    for sector in expected_sectors:
        assert sector in sectors
```

---

#### Test Suite: Screen Stocks - Basic Filtering
```python
def test_screen_stocks_no_filters():
    """Test screening with no filters returns all stocks"""
    response = client.post('/api/screen', json={})
    assert response.status_code == 200
    assert len(response.json) == 18

def test_screen_stocks_empty_body():
    """Test screening with None body returns all stocks"""
    response = client.post('/api/screen', json=None)
    assert response.status_code == 200
    assert len(response.json) == 18

def test_filter_by_min_market_cap():
    """Test filtering by minimum market cap"""
    response = client.post('/api/screen', json={'min_market_cap': 1000})
    assert response.status_code == 200
    # All returned stocks should have market_cap >= 1000
    for stock in response.json:
        assert stock['market_cap'] >= 1000

def test_filter_by_max_market_cap():
    """Test filtering by maximum market cap"""
    response = client.post('/api/screen', json={'max_market_cap': 100})
    assert response.status_code == 200
    # All returned stocks should have market_cap <= 100
    for stock in response.json:
        assert stock['market_cap'] <= 100

def test_filter_by_market_cap_range():
    """Test filtering by market cap range"""
    response = client.post('/api/screen', json={
        'min_market_cap': 100,
        'max_market_cap': 500
    })
    assert response.status_code == 200
    for stock in response.json:
        assert 100 <= stock['market_cap'] <= 500
```

---

#### Test Suite: Screen Stocks - P/E and P/S Filtering
```python
def test_filter_by_min_pe_ratio():
    """Test filtering by minimum P/E ratio"""
    response = client.post('/api/screen', json={'min_pe_ratio': 30})
    assert response.status_code == 200
    # All returned stocks with pe_ratio should have value >= 30
    for stock in response.json:
        if stock['pe_ratio'] is not None:
            assert stock['pe_ratio'] >= 30

def test_filter_by_max_pe_ratio():
    """Test filtering by maximum P/E ratio"""
    response = client.post('/api/screen', json={'max_pe_ratio': 25})
    assert response.status_code == 200
    for stock in response.json:
        if stock['pe_ratio'] is not None:
            assert stock['pe_ratio'] <= 25

def test_filter_excludes_null_pe_ratios():
    """Test that min/max PE filters exclude stocks with null PE"""
    response = client.post('/api/screen', json={'min_pe_ratio': 10})
    assert response.status_code == 200
    # No stock with null pe_ratio should be in results
    for stock in response.json:
        assert stock['pe_ratio'] is not None

def test_filter_by_ps_ratio_range():
    """Test filtering by P/S ratio range"""
    response = client.post('/api/screen', json={
        'min_ps_ratio': 5,
        'max_ps_ratio': 10
    })
    assert response.status_code == 200
    for stock in response.json:
        if stock['ps_ratio'] is not None:
            assert 5 <= stock['ps_ratio'] <= 10
```

---

#### Test Suite: Screen Stocks - Growth and Sentiment
```python
def test_filter_by_min_revenue_growth():
    """Test filtering by minimum revenue growth"""
    response = client.post('/api/screen', json={'min_revenue_growth': 15})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['revenue_growth'] >= 15

def test_filter_by_negative_revenue_growth():
    """Test filtering allows negative revenue growth values"""
    response = client.post('/api/screen', json={'min_revenue_growth': -10})
    assert response.status_code == 200
    # Should return stocks with revenue_growth >= -10
    for stock in response.json:
        assert stock['revenue_growth'] >= -10

def test_filter_by_min_sentiment():
    """Test filtering by minimum sentiment score"""
    response = client.post('/api/screen', json={'min_sentiment_score': 0.6})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['sentiment_score'] >= 0.6

def test_filter_by_sentiment_range():
    """Test sentiment filtering with valid range"""
    response = client.post('/api/screen', json={'min_sentiment_score': 0.5})
    assert response.status_code == 200
    for stock in response.json:
        assert -1 <= stock['sentiment_score'] <= 1
        assert stock['sentiment_score'] >= 0.5
```

---

#### Test Suite: Screen Stocks - Sector and Guidance
```python
def test_filter_by_single_sector():
    """Test filtering by single sector"""
    response = client.post('/api/screen', json={'sectors': ['Software']})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['sector'] == 'Software'

def test_filter_by_multiple_sectors():
    """Test filtering by multiple sectors"""
    sectors = ['Software', 'Semiconductors']
    response = client.post('/api/screen', json={'sectors': sectors})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['sector'] in sectors

def test_filter_by_empty_sectors_list():
    """Test that empty sectors list returns all stocks"""
    response = client.post('/api/screen', json={'sectors': []})
    assert response.status_code == 200
    assert len(response.json) == 18

def test_filter_by_management_guidance_positive():
    """Test filtering by positive management guidance"""
    response = client.post('/api/screen', json={'management_guidance': 'positive'})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['management_guidance'] == 'positive'

def test_filter_by_management_guidance_neutral():
    """Test filtering by neutral management guidance"""
    response = client.post('/api/screen', json={'management_guidance': 'neutral'})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['management_guidance'] == 'neutral'

def test_filter_by_management_guidance_negative():
    """Test filtering by negative management guidance"""
    response = client.post('/api/screen', json={'management_guidance': 'negative'})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['management_guidance'] == 'negative'
```

---

#### Test Suite: Screen Stocks - Complex Filtering
```python
def test_filter_multiple_criteria():
    """Test filtering with multiple criteria simultaneously"""
    filters = {
        'min_market_cap': 100,
        'max_market_cap': 2000,
        'min_pe_ratio': 20,
        'max_pe_ratio': 60,
        'min_revenue_growth': 10,
        'min_sentiment_score': 0.5,
        'sectors': ['Software', 'Semiconductors'],
        'management_guidance': 'positive'
    }
    response = client.post('/api/screen', json=filters)
    assert response.status_code == 200

    # Verify each filter is applied
    for stock in response.json:
        assert 100 <= stock['market_cap'] <= 2000
        if stock['pe_ratio']:
            assert 20 <= stock['pe_ratio'] <= 60
        assert stock['revenue_growth'] >= 10
        assert stock['sentiment_score'] >= 0.5
        assert stock['sector'] in ['Software', 'Semiconductors']
        assert stock['management_guidance'] == 'positive'

def test_filter_no_matches():
    """Test filtering that returns zero results"""
    filters = {
        'min_market_cap': 10000,  # No stock has this market cap
    }
    response = client.post('/api/screen', json=filters)
    assert response.status_code == 200
    assert len(response.json) == 0
    assert response.json == []

def test_filter_invalid_range():
    """Test filtering with min > max returns empty results"""
    filters = {
        'min_market_cap': 1000,
        'max_market_cap': 100  # Invalid: min > max
    }
    response = client.post('/api/screen', json=filters)
    assert response.status_code == 200
    assert len(response.json) == 0
```

---

#### Test Suite: Get Statistics
```python
def test_get_stats_returns_200():
    """Test that /api/stats returns 200"""
    response = client.get('/api/stats')
    assert response.status_code == 200

def test_get_stats_structure():
    """Test that stats response has correct structure"""
    response = client.get('/api/stats')
    data = response.json
    assert 'total_stocks' in data
    assert 'average_pe' in data
    assert 'average_sentiment' in data
    assert 'guidance_breakdown' in data

def test_get_stats_total_stocks():
    """Test that total_stocks is correct"""
    response = client.get('/api/stats')
    assert response.json['total_stocks'] == 18

def test_get_stats_average_pe_valid():
    """Test that average_pe is a valid number"""
    response = client.get('/api/stats')
    avg_pe = response.json['average_pe']
    assert isinstance(avg_pe, (int, float))
    assert avg_pe > 0

def test_get_stats_average_sentiment_range():
    """Test that average_sentiment is within valid range"""
    response = client.get('/api/stats')
    avg_sentiment = response.json['average_sentiment']
    assert -1 <= avg_sentiment <= 1

def test_get_stats_guidance_breakdown():
    """Test guidance breakdown structure and totals"""
    response = client.get('/api/stats')
    breakdown = response.json['guidance_breakdown']
    assert 'positive' in breakdown
    assert 'neutral' in breakdown
    assert 'negative' in breakdown
    # Total should equal total stocks
    total = breakdown['positive'] + breakdown['neutral'] + breakdown['negative']
    assert total == 18
```

---

### 6.2 Frontend Tests

#### Test Suite: Application Initialization
```javascript
describe('Application Initialization', () => {
  test('should load all stocks on page load', async () => {
    // Mock API response
    // Load app
    // Assert allStocks array is populated
  });

  test('should load stats on page load', async () => {
    // Mock /api/stats response
    // Load app
    // Assert stats are displayed correctly
  });

  test('should load sectors for filter checkboxes', async () => {
    // Mock /api/sectors response
    // Load app
    // Assert sector checkboxes are rendered
  });

  test('should restore dark mode from localStorage', () => {
    // Set localStorage darkMode = 'true'
    // Load app
    // Assert data-theme attribute is 'dark'
  });

  test('should restore watchlist from localStorage', () => {
    // Set localStorage watchlist = ['AAPL', 'MSFT']
    // Load app
    // Assert watchlist count is 2
  });
});
```

---

#### Test Suite: Theme Toggle
```javascript
describe('Theme Toggle', () => {
  test('should toggle to dark mode when button clicked', () => {
    // Click theme toggle button
    // Assert data-theme attribute is 'dark'
    // Assert icon changed to sun
  });

  test('should toggle back to light mode', () => {
    // Set dark mode
    // Click theme toggle button
    // Assert data-theme attribute removed
    // Assert icon changed to moon
  });

  test('should persist theme preference to localStorage', () => {
    // Click theme toggle button
    // Assert localStorage.darkMode === 'true'
  });
});
```

---

#### Test Suite: Stock Filtering
```javascript
describe('Stock Filtering', () => {
  test('should filter stocks by market cap', async () => {
    // Set minMarketCap input to 1000
    // Click Apply Filters
    // Assert filtered stocks all have market_cap >= 1000
  });

  test('should filter stocks by multiple criteria', async () => {
    // Set multiple filter inputs
    // Click Apply Filters
    // Assert all filters are applied correctly
  });

  test('should show "No stocks match" when no results', async () => {
    // Set impossible filter criteria
    // Click Apply Filters
    // Assert table shows "No stocks match your filters"
  });

  test('should reset all filters when Reset clicked', () => {
    // Set multiple filters
    // Click Reset All
    // Assert all input values are cleared
    // Assert all stocks are displayed
  });

  test('should update result count after filtering', async () => {
    // Apply filters that return 5 stocks
    // Assert resultCount element shows "5"
  });
});
```

---

#### Test Suite: Watchlist Management
```javascript
describe('Watchlist Management', () => {
  test('should add stock to watchlist when star clicked', () => {
    // Click star icon for AAPL
    // Assert watchlist includes 'AAPL'
    // Assert star icon is filled
  });

  test('should remove stock from watchlist when star clicked again', () => {
    // Add AAPL to watchlist
    // Click star icon for AAPL
    // Assert watchlist does not include 'AAPL'
    // Assert star icon is empty
  });

  test('should persist watchlist to localStorage', () => {
    // Add stocks to watchlist
    // Assert localStorage.watchlist is updated
  });

  test('should update watchlist count badge', () => {
    // Add 3 stocks to watchlist
    // Assert watchlistCount element shows "3"
  });

  test('should show watchlist modal when button clicked', () => {
    // Click Watchlist button
    // Assert watchlist modal is visible
  });

  test('should display empty state when watchlist is empty', () => {
    // Clear watchlist
    // Open watchlist modal
    // Assert empty state message is shown
  });

  test('should display watchlist stocks with details', () => {
    // Add stocks to watchlist
    // Open watchlist modal
    // Assert stock details are displayed correctly
  });
});
```

---

#### Test Suite: Stock Details Modal
```javascript
describe('Stock Details Modal', () => {
  test('should open modal when ticker clicked', () => {
    // Click ticker in table
    // Assert stock modal is visible
  });

  test('should open modal when View button clicked', () => {
    // Click View button
    // Assert stock modal is visible
  });

  test('should display all stock metrics', () => {
    // Open modal for AAPL
    // Assert all 12 metrics are displayed
  });

  test('should close modal when X button clicked', () => {
    // Open modal
    // Click close button
    // Assert modal is not visible
  });

  test('should close modal when clicking outside', () => {
    // Open modal
    // Click modal overlay
    // Assert modal is not visible
  });

  test('should allow adding to watchlist from modal', () => {
    // Open modal for stock not in watchlist
    // Click "Add to Watchlist" button
    // Assert stock is added to watchlist
    // Assert button text changes to "Remove from Watchlist"
  });
});
```

---

#### Test Suite: CSV Export
```javascript
describe('CSV Export', () => {
  test('should export filtered stocks to CSV', () => {
    // Filter to 5 stocks
    // Click Export CSV button
    // Assert CSV file is downloaded
    // Assert CSV contains 5 data rows + 1 header row
  });

  test('should include correct headers in CSV', () => {
    // Click Export CSV
    // Assert CSV headers match expected columns
  });

  test('should format CSV data correctly', () => {
    // Click Export CSV
    // Assert values are comma-separated
    // Assert N/A values for null fields
  });

  test('should use current date in filename', () => {
    // Click Export CSV
    // Assert filename includes current date
  });
});
```

---

#### Test Suite: Error Handling
```javascript
describe('Error Handling', () => {
  test('should show error message when API is unreachable', async () => {
    // Mock failed fetch request
    // Load app
    // Assert error message is displayed in table
  });

  test('should handle localStorage unavailability gracefully', () => {
    // Mock localStorage.getItem to throw error
    // Load app
    // Assert app still loads with default values
  });

  test('should handle invalid watchlist data in localStorage', () => {
    // Set localStorage.watchlist to invalid JSON
    // Load app
    // Assert watchlist defaults to empty array
  });
});
```

---

### 6.3 Integration Tests

#### Test Suite: End-to-End User Flows
```javascript
describe('E2E: Stock Screening Flow', () => {
  test('User can filter stocks and view details', async () => {
    // 1. Load app
    // 2. Set filter: min revenue growth = 15%
    // 3. Click Apply Filters
    // 4. Assert results are filtered
    // 5. Click first stock ticker
    // 6. Assert modal opens with correct data
    // 7. Close modal
    // 8. Assert modal is closed
  });

  test('User can build a watchlist', async () => {
    // 1. Load app
    // 2. Add 3 stocks to watchlist
    // 3. Assert watchlist count is 3
    // 4. Open watchlist modal
    // 5. Assert 3 stocks are displayed
    // 6. Remove 1 stock
    // 7. Assert watchlist count is 2
    // 8. Refresh page
    // 9. Assert watchlist count is still 2 (persistence)
  });

  test('User can export filtered results', async () => {
    // 1. Load app
    // 2. Apply filters
    // 3. Click Export CSV
    // 4. Assert CSV download is triggered
    // 5. Assert CSV content matches filtered stocks
  });

  test('User can toggle dark mode', () => {
    // 1. Load app in light mode
    // 2. Click theme toggle
    // 3. Assert dark mode is applied
    // 4. Refresh page
    // 5. Assert dark mode persists
  });
});
```

---

## 7. Implementation Checklist

### Phase 1: Backend Setup
- [ ] Initialize Flask application with CORS
- [ ] Define Stock and ScreenerFilter models
- [ ] Create mock data for 18 NASDAQ tech stocks
- [ ] Implement GET /health endpoint
- [ ] Implement GET /api/stocks endpoint
- [ ] Implement GET /api/stocks/<ticker> endpoint
- [ ] Implement GET /api/sectors endpoint
- [ ] Implement POST /api/screen endpoint with filtering logic
- [ ] Implement GET /api/stats endpoint
- [ ] Write unit tests for all endpoints
- [ ] Test null value handling in filters

### Phase 2: Frontend Core
- [ ] Create HTML structure with semantic markup
- [ ] Build CSS with light/dark theme variables
- [ ] Implement API client with fetch
- [ ] Load and display all stocks in table
- [ ] Load and display market statistics
- [ ] Load sector filters dynamically
- [ ] Implement theme toggle with persistence
- [ ] Format currency and percentage values
- [ ] Handle null/N/A values in display

### Phase 3: Filtering Features
- [ ] Build filter sidebar UI
- [ ] Implement filter input handling
- [ ] Send filter request to backend
- [ ] Update table with filtered results
- [ ] Implement reset filters functionality
- [ ] Show result count
- [ ] Display empty state for no results
- [ ] Add loading states

### Phase 4: Watchlist
- [ ] Implement watchlist state management
- [ ] Add star icons to table rows
- [ ] Implement add/remove from watchlist
- [ ] Persist watchlist to localStorage
- [ ] Update watchlist count badge
- [ ] Build watchlist modal UI
- [ ] Display watchlist items with details
- [ ] Handle empty watchlist state

### Phase 5: Modals & Details
- [ ] Build stock details modal
- [ ] Populate modal with stock data
- [ ] Implement modal open/close
- [ ] Add watchlist toggle in modal
- [ ] Build watchlist modal
- [ ] Implement click-outside-to-close
- [ ] Style modals responsively

### Phase 6: Export & Polish
- [ ] Implement CSV export functionality
- [ ] Generate CSV from filtered stocks
- [ ] Trigger browser download
- [ ] Add responsive design breakpoints
- [ ] Test on mobile/tablet
- [ ] Add color coding for positive/negative values
- [ ] Implement sentiment badges
- [ ] Implement guidance badges
- [ ] Add loading and error states

### Phase 7: Testing & Documentation
- [ ] Write backend unit tests (all endpoints)
- [ ] Write frontend unit tests (components)
- [ ] Write integration tests (user flows)
- [ ] Test edge cases (null values, empty results)
- [ ] Test error handling (API down, invalid data)
- [ ] Test localStorage persistence
- [ ] Create user documentation
- [ ] Create API documentation

---

## 8. Future Enhancements (Post-MVP)

### High Priority
- Real-time data integration (Alpha Vantage, IEX Cloud, or similar API)
- Historical price charts (line/candlestick)
- User authentication and accounts
- Saved custom screens
- Email alerts for watchlist stocks
- Price alerts

### Medium Priority
- Advanced sentiment analysis (news, social media)
- More detailed management guidance (earnings call transcripts)
- Comparison tool (compare 2-4 stocks side-by-side)
- Mobile app (React Native or PWA)
- Database integration (PostgreSQL)
- Backend caching (Redis)

### Low Priority
- Stock recommendations based on criteria
- Backtesting filters against historical data
- Portfolio tracking
- Technical indicators (RSI, MACD, etc.)
- Screener presets (value stocks, growth stocks, etc.)

---

## 9. Technical Debt & Optimizations

### Known Limitations
1. **No Input Validation:** Frontend doesn't validate min < max for range filters
2. **No Request Debouncing:** Rapid filter changes can cause multiple API calls
3. **No Loading States:** Buttons don't disable during API requests
4. **No Error Retry:** Failed API calls don't retry automatically
5. **No ESC Key Support:** Modals can't be closed with ESC key
6. **No Pagination:** All stocks loaded at once (acceptable for 18 stocks, not for 500+)

### Recommended Optimizations
1. Add client-side filter validation
2. Implement request debouncing (300ms delay)
3. Add loading spinners and disabled states
4. Implement exponential backoff for failed requests
5. Add keyboard navigation support
6. Prepare for pagination if stock count grows

---

## 10. Deployment Considerations

### Development
- Backend: `python src/app.py` (localhost:5000)
- Frontend: Open `frontend/index.html` or use `python -m http.server`

### Production (Future)
- Backend: Deploy to Heroku, AWS, GCP, or similar
- Frontend: Deploy to Netlify, Vercel, or S3 + CloudFront
- Database: Migrate from mock data to PostgreSQL
- Caching: Add Redis for API response caching
- CDN: Serve static assets from CDN
- Environment Variables: API keys, database URLs
- HTTPS: Enable SSL/TLS
- CORS: Configure allowed origins properly
- Rate Limiting: Prevent abuse
- Monitoring: Add error tracking (Sentry) and analytics

---

## Document Version
**Version:** 1.0
**Date:** 2025-11-09
**Status:** MVP Implementation Ready
