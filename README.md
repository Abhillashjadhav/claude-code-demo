# NASDAQ Tech Screener Application

A modern, web-based application that tracks daily valuations of NASDAQ-listed tech companies and screens for high-potential, undervalued stocks using quantitative and qualitative signals.

## Features

### Core Functionality
- **Real-time Stock Screening**: Filter NASDAQ tech stocks by multiple criteria including P/E ratio, P/S ratio, market cap, revenue growth, and sentiment
- **Valuation Metrics**: Comprehensive valuation data including P/E, P/S, P/B ratios, EV/EBITDA, and growth metrics
- **Sentiment Analysis**: Track market sentiment scores and trends for each stock
- **Management Guidance**: View management outlook (positive, neutral, negative) for companies
- **Watchlist**: Save favorite stocks to a personal watchlist with local storage persistence
- **Stock Details**: Detailed view of individual stock metrics and performance indicators
- **Export Functionality**: Export filtered results to CSV for further analysis

### User Experience
- **Dark Mode**: Toggle between light and dark themes with preference persistence
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Interactive Filters**: Real-time filtering with multiple criteria
- **Clean UI**: Modern, intuitive interface built with vanilla JavaScript and CSS
- **Performance Stats**: Dashboard showing overall market statistics

## Technology Stack

### Backend
- **Flask**: Python web framework for API endpoints
- **Flask-CORS**: Cross-origin resource sharing support
- **Python 3.x**: Core backend language

### Frontend
- **HTML5/CSS3**: Modern semantic markup and styling
- **Vanilla JavaScript**: No framework dependencies, pure JS for performance
- **LocalStorage**: Client-side data persistence for watchlist and preferences

### Data
- Mock NASDAQ tech stock data (18 companies including AAPL, MSFT, NVDA, GOOGL, META, etc.)
- Realistic valuation metrics and growth indicators

## Project Structure

```
claude-code-demo/
├── src/                    # Backend source code
│   ├── app.py             # Flask API server
│   ├── models.py          # Data models
│   ├── data.py            # Mock stock data
│   └── tests/             # Backend tests
├── frontend/              # Frontend application
│   ├── index.html         # Main HTML file
│   ├── css/
│   │   └── styles.css     # Styles with dark mode support
│   └── js/
│       └── app.js         # Application logic
├── Requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- A modern web browser (Chrome, Firefox, Safari, or Edge)

### Backend Setup

1. **Install Python dependencies**:
```bash
pip install -r Requirements.txt
```

2. **Run the Flask API server**:
```bash
cd src
python app.py
```

The API server will start on `http://localhost:5000`

### Frontend Setup

1. **Open the frontend**:
   - Option 1: Simply open `frontend/index.html` in your web browser
   - Option 2: Use a local web server (recommended):
```bash
cd frontend
python -m http.server 8000
```
   Then navigate to `http://localhost:8000`

## Usage

### Screening Stocks

1. **View All Stocks**: Upon loading, all stocks are displayed in the main table
2. **Apply Filters**: Use the left sidebar to filter stocks by:
   - Market Cap range
   - P/E Ratio range
   - P/S Ratio range
   - Minimum Revenue Growth
   - Minimum Sentiment Score
   - Specific Sectors
   - Management Guidance outlook
3. **Click "Apply Filters"** to see filtered results
4. **Reset Filters** to clear all criteria and show all stocks again

### Watchlist Management

1. **Add to Watchlist**: Click the star (☆) icon next to any stock
2. **View Watchlist**: Click the "Watchlist" button in the header
3. **Remove from Watchlist**: Click the filled star (★) or remove from the watchlist modal

### Stock Details

1. Click on any ticker symbol or the "View" button
2. See comprehensive metrics including:
   - Valuation ratios
   - Growth metrics
   - Sentiment and guidance information
   - Trading volume

### Export Data

Click the "Export CSV" button to download the current filtered results as a CSV file for further analysis.

### Dark Mode

Click the moon/sun icon in the header to toggle between light and dark themes. Your preference is saved automatically.

## API Endpoints

### GET `/health`
Health check endpoint
- Returns: `{"status": "ok"}`

### GET `/api/stocks`
Get all stocks
- Returns: Array of stock objects

### GET `/api/stocks/<ticker>`
Get specific stock by ticker
- Parameters: `ticker` (string)
- Returns: Single stock object or 404 if not found

### GET `/api/sectors`
Get all unique sectors
- Returns: Array of sector names

### POST `/api/screen`
Screen stocks with filters
- Body: Filter criteria object
- Returns: Array of filtered stock objects

### GET `/api/stats`
Get market statistics
- Returns: Overall market stats including average P/E, sentiment, and guidance breakdown

## Filter Criteria

The screening endpoint accepts the following filter parameters:

```json
{
  "min_market_cap": 100,        // Minimum market cap in billions
  "max_market_cap": 1000,       // Maximum market cap in billions
  "min_pe_ratio": 10,           // Minimum P/E ratio
  "max_pe_ratio": 50,           // Maximum P/E ratio
  "min_ps_ratio": 5,            // Minimum P/S ratio
  "max_ps_ratio": 20,           // Maximum P/S ratio
  "min_revenue_growth": 10,     // Minimum revenue growth %
  "min_sentiment_score": 0.5,   // Minimum sentiment (-1 to 1)
  "sectors": ["Software"],      // Array of sectors to include
  "management_guidance": "positive"  // "positive", "neutral", or "negative"
}
```

## Development

### Running Tests

```bash
cd src
pytest
```

### Adding New Stocks

Edit `src/data.py` and add new `Stock` objects to the `MOCK_STOCKS` list.

### Customizing the UI

- **Colors & Theme**: Edit CSS variables in `frontend/css/styles.css`
- **Layout**: Modify `frontend/index.html`
- **Behavior**: Update `frontend/js/app.js`

## Roadmap

### Phase 1: MVP (Complete)
- ✅ Core screener functionality
- ✅ Multi-criteria filtering
- ✅ Watchlist with local storage
- ✅ Dark mode support
- ✅ Responsive design
- ✅ CSV export

### Phase 2: Enhanced Features (Planned)
- [ ] User authentication
- [ ] Saved custom screens
- [ ] Email alerts for watchlist stocks
- [ ] Historical price charts
- [ ] Real-time data integration with financial APIs
- [ ] Advanced sentiment analysis
- [ ] More detailed management guidance

### Phase 3: Production (Planned)
- [ ] Database integration
- [ ] User accounts and preferences
- [ ] Real-time WebSocket updates
- [ ] Mobile app (React Native)
- [ ] Premium features

## Contributing

This is a demo project. For production use, consider:
1. Integrating with real financial data APIs (Alpha Vantage, IEX Cloud, etc.)
2. Adding user authentication and database storage
3. Implementing rate limiting and caching
4. Adding comprehensive error handling
5. Writing more extensive tests

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please open an issue on the GitHub repository.

---

**Note**: This application uses mock data for demonstration purposes. For real trading decisions, always use verified, real-time data from reliable financial data providers.