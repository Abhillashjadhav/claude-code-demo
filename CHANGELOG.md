# Changelog

All notable changes to the NASDAQ Tech Screener application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-11-09

### MVP Release - Initial Public Release

This is the first complete release of the NASDAQ Tech Screener application, a modern web-based stock screening tool for NASDAQ-listed technology companies.

### Added

#### Backend API (Flask)
- **6 RESTful API Endpoints**:
  - `GET /health` - Health check endpoint for API status verification
  - `GET /api/stocks` - Retrieve all 18 NASDAQ tech stocks with complete metrics
  - `GET /api/stocks/<ticker>` - Get detailed information for a specific stock by ticker symbol (case-insensitive)
  - `GET /api/sectors` - Retrieve list of all unique sectors from available stocks
  - `POST /api/screen` - Advanced multi-criteria stock screening with flexible filters
  - `GET /api/stats` - Get aggregated market statistics (average P/E, sentiment, guidance breakdown)

- **Data Models**:
  - `Stock` dataclass with 16 comprehensive fields including valuation ratios, growth metrics, sentiment, and guidance
  - `ScreenerFilter` dataclass for validating and processing filter criteria
  - Proper null handling for unprofitable companies (P/E, P/S, P/B, EV/EBITDA can be None)

- **Mock Data**:
  - 18 realistic NASDAQ tech stocks (AAPL, MSFT, NVDA, GOOGL, META, AMZN, TSLA, ADBE, CRM, NFLX, INTC, AMD, PYPL, SHOP, SQ, SPOT, SNOW, ZM)
  - Diverse sectors: Consumer Electronics, Software, Semiconductors, Internet Services, Social Media, E-Commerce, Cloud Software, FinTech, and more
  - Realistic valuation metrics based on 2025 market conditions
  - Mix of profitable and unprofitable companies for comprehensive testing

- **CORS Support**: Full cross-origin resource sharing enabled for frontend-backend communication

#### Frontend Application (HTML/CSS/JavaScript)
- **Responsive Single-Page Application**:
  - Clean, modern interface built with vanilla HTML5, CSS3, and JavaScript
  - No framework dependencies for optimal performance and simplicity
  - Fully responsive design for desktop, tablet, and mobile devices

- **Dashboard & Statistics**:
  - Real-time market statistics display (total stocks, average P/E, average sentiment, positive guidance count)
  - Auto-loading on application initialization

- **Advanced Stock Screener**:
  - **7 Filter Criteria**:
    - Market Cap range (min/max in billions)
    - P/E Ratio range (min/max)
    - P/S Ratio range (min/max)
    - Minimum Revenue Growth percentage
    - Minimum Sentiment Score (-1 to 1 scale)
    - Sector selection (multi-select checkboxes)
    - Management Guidance filter (positive/neutral/negative)
  - Real-time filtering with instant table updates
  - Result count display
  - Reset all filters functionality

- **Interactive Results Table**:
  - 11 columns: Ticker, Company, Sector, Price, Market Cap, P/E, P/S, Revenue Growth, Sentiment, Guidance, Actions
  - Clickable ticker symbols for stock details
  - Color-coded metrics:
    - Green for positive revenue growth
    - Red for negative revenue growth
    - Sentiment badges with trend indicators (up/down/stable)
    - Guidance badges (positive/neutral/negative) with appropriate styling
  - Proper N/A display for null values (unprofitable companies)
  - Empty state message when no stocks match filters
  - Loading state during data fetch

- **Watchlist Management**:
  - Add/remove stocks with star icon toggle
  - Watchlist count badge in header
  - Dedicated watchlist modal with:
    - Empty state message when no stocks saved
    - Stock details (ticker, name, price, revenue growth)
    - Quick view and remove actions
    - Navigation to stock details from watchlist
  - Persistent storage using browser localStorage
  - Automatic state synchronization across all UI components

- **Stock Details Modal**:
  - Comprehensive 12-metric grid display:
    - Current Price, Market Cap, P/E Ratio, P/S Ratio, P/B Ratio, EV/EBITDA
    - Revenue Growth %, Earnings Growth %, Trading Volume
    - Sector, Sentiment Score (with trend), Management Guidance
  - Add/remove from watchlist directly in modal
  - Click outside or close button to dismiss
  - Proper formatting for currency, percentages, and large numbers

- **CSV Export**:
  - Export currently filtered stocks (not all stocks)
  - Automatic filename with date: `nasdaq-tech-screener-YYYY-MM-DD.csv`
  - Includes 10 key columns: Ticker, Company, Sector, Price, Market Cap, P/E, P/S, Revenue Growth, Sentiment, Guidance
  - Proper CSV formatting with headers
  - Handles null values gracefully (displays as "N/A")
  - Browser download trigger

- **Dark Mode Theme**:
  - Toggle button in header with sun/moon icons
  - Smooth transitions between light and dark themes
  - Complete color scheme for both modes
  - Theme preference persisted to localStorage
  - Auto-restore theme on page load

- **User Experience Enhancements**:
  - Professional typography using Inter font family
  - Smooth hover effects and transitions
  - Accessible button states and focus indicators
  - Modal overlays with backdrop blur
  - Responsive breakpoints for mobile optimization

#### Testing & Quality Assurance
- **40 Comprehensive Backend Tests**:
  - Health check endpoint validation
  - All stocks retrieval (count, structure, status codes)
  - Stock by ticker (success, case-insensitivity, 404 handling)
  - Sectors endpoint (uniqueness, expected values)
  - Basic filtering (no filters, empty body, market cap ranges)
  - P/E and P/S ratio filtering (including null value exclusion)
  - Growth and sentiment filtering (including negative values)
  - Sector and guidance filtering (single, multiple, empty)
  - Complex multi-criteria filtering
  - Edge cases (no matches, invalid ranges)
  - Statistics endpoint (structure, calculations, totals)
- **100% Test Pass Rate**: All 40 tests passing
- **Test Coverage**: All API endpoints, filters, edge cases, and error conditions

#### Documentation
- Comprehensive `docs/requirements.md` with:
  - Problem statement and goals
  - Complete API endpoint specifications
  - Data models and validation rules
  - Frontend component specifications
  - Edge case handling guidelines
  - Test case specifications
  - Implementation checklist
  - Future enhancement roadmap
- Detailed `README.md` with:
  - Feature overview
  - Technology stack
  - Installation and setup instructions
  - Usage guide
  - API endpoint reference
  - Development guidelines

### Technical Details

#### Dependencies
- **Backend**:
  - Flask (web framework)
  - Flask-CORS (CORS support)
  - pytest (testing)
- **Frontend**:
  - No external dependencies (vanilla JavaScript)
  - Uses browser built-in features: fetch API, localStorage, CSS Grid/Flexbox

#### Architecture
- **Backend**: RESTful API with stateless endpoint design
- **Frontend**: Client-side rendering with separation of concerns
- **Data Flow**:
  1. Frontend fetches data from Flask API
  2. State management in JavaScript
  3. Local persistence using browser storage
  4. Real-time UI updates without page refresh

#### Performance
- All filtering operations complete in under 1 second
- Lightweight frontend (no framework overhead)
- Efficient data structures and algorithms
- Minimal API calls with client-side filtering

### Known Limitations

The following limitations are documented for future enhancement:

1. **Mock Data Only**: Uses 18 hardcoded stocks instead of real-time API integration
2. **No Input Validation**: Frontend doesn't validate min < max for range filters
3. **No Request Debouncing**: Rapid filter changes can cause multiple API calls
4. **No Loading States on Buttons**: Buttons don't disable during API requests
5. **No ESC Key Support**: Modals can't be closed with ESC key
6. **No Pagination**: All stocks loaded at once (acceptable for 18 stocks, not scalable to 500+)
7. **Client-Side Only**: No user authentication or server-side user data persistence

### Future Enhancements

Planned features for future releases:

#### High Priority (v2.0.0)
- Real-time data integration with financial APIs (Alpha Vantage, IEX Cloud, or similar)
- Historical price charts (line/candlestick)
- User authentication and accounts
- Saved custom screening criteria
- Email alerts for watchlist stocks
- Price alerts

#### Medium Priority (v2.x)
- Advanced sentiment analysis from news and social media
- Stock comparison tool (side-by-side comparison)
- Mobile app (React Native or PWA)
- Database integration (PostgreSQL)
- Backend caching (Redis)
- Pagination for large result sets

#### Low Priority (v3.x)
- AI-powered stock recommendations
- Backtesting filters against historical data
- Portfolio tracking
- Technical indicators (RSI, MACD, moving averages)
- Preset screening strategies (value, growth, momentum)

### Installation & Upgrade

#### Fresh Installation
```bash
# Install backend dependencies
pip install -r Requirements.txt

# Run backend server
cd src
python app.py

# Open frontend
# Option 1: Open frontend/index.html in browser
# Option 2: Use local web server
cd frontend
python -m http.server 8000
```

#### Running Tests
```bash
cd src
pytest
# Expected: 40 tests passed
```

### Contributors

Initial release developed as part of the NASDAQ Tech Screener MVP project.

### License

MIT License - See LICENSE file for details

---

## [Unreleased]

### Planned for v1.1.0
- Client-side input validation for filter ranges
- Request debouncing for filter operations
- Loading spinners and disabled button states during API calls
- ESC key support for closing modals
- Keyboard navigation improvements
- Error retry mechanism with exponential backoff

---

**Note**: This application currently uses mock data for demonstration purposes. For real trading decisions, always use verified, real-time data from reliable financial data providers.
