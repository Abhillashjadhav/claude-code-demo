"""Mock data for NASDAQ tech stocks"""
from models import Stock
from datetime import datetime

# Mock NASDAQ tech stocks with realistic valuations
MOCK_STOCKS = [
    Stock(
        ticker="AAPL",
        name="Apple Inc.",
        sector="Consumer Electronics",
        market_cap=2800.5,
        price=178.25,
        pe_ratio=28.5,
        ps_ratio=7.2,
        pb_ratio=45.3,
        ev_ebitda=22.1,
        revenue_growth=8.2,
        earnings_growth=12.5,
        sentiment_score=0.75,
        sentiment_trend="up",
        management_guidance="positive",
        volume=52000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="MSFT",
        name="Microsoft Corporation",
        sector="Software",
        market_cap=2750.3,
        price=368.50,
        pe_ratio=32.4,
        ps_ratio=11.5,
        pb_ratio=12.8,
        ev_ebitda=24.3,
        revenue_growth=15.2,
        earnings_growth=18.7,
        sentiment_score=0.82,
        sentiment_trend="up",
        management_guidance="positive",
        volume=23000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="NVDA",
        name="NVIDIA Corporation",
        sector="Semiconductors",
        market_cap=1150.2,
        price=475.80,
        pe_ratio=72.5,
        ps_ratio=35.2,
        pb_ratio=48.7,
        ev_ebitda=65.4,
        revenue_growth=125.5,
        earnings_growth=215.3,
        sentiment_score=0.88,
        sentiment_trend="up",
        management_guidance="positive",
        volume=45000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="GOOGL",
        name="Alphabet Inc.",
        sector="Internet Services",
        market_cap=1680.7,
        price=138.45,
        pe_ratio=24.8,
        ps_ratio=5.8,
        pb_ratio=6.2,
        ev_ebitda=14.5,
        revenue_growth=11.3,
        earnings_growth=14.2,
        sentiment_score=0.65,
        sentiment_trend="stable",
        management_guidance="neutral",
        volume=28000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="META",
        name="Meta Platforms Inc.",
        sector="Social Media",
        market_cap=850.4,
        price=325.75,
        pe_ratio=22.3,
        ps_ratio=7.1,
        pb_ratio=5.8,
        ev_ebitda=13.2,
        revenue_growth=22.5,
        earnings_growth=145.8,
        sentiment_score=0.55,
        sentiment_trend="up",
        management_guidance="positive",
        volume=18000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="AMZN",
        name="Amazon.com Inc.",
        sector="E-Commerce",
        market_cap=1520.8,
        price=148.25,
        pe_ratio=58.7,
        ps_ratio=2.8,
        pb_ratio=7.9,
        ev_ebitda=18.5,
        revenue_growth=12.4,
        earnings_growth=385.2,
        sentiment_score=0.68,
        sentiment_trend="up",
        management_guidance="positive",
        volume=42000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="TSLA",
        name="Tesla Inc.",
        sector="Electric Vehicles",
        market_cap=685.3,
        price=215.50,
        pe_ratio=62.4,
        ps_ratio=7.5,
        pb_ratio=14.2,
        ev_ebitda=35.8,
        revenue_growth=18.8,
        earnings_growth=92.5,
        sentiment_score=0.72,
        sentiment_trend="up",
        management_guidance="positive",
        volume=95000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="ADBE",
        name="Adobe Inc.",
        sector="Software",
        market_cap=225.6,
        price=495.30,
        pe_ratio=42.1,
        ps_ratio=12.8,
        pb_ratio=15.3,
        ev_ebitda=28.7,
        revenue_growth=10.5,
        earnings_growth=13.2,
        sentiment_score=0.58,
        sentiment_trend="stable",
        management_guidance="neutral",
        volume=3200000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="CRM",
        name="Salesforce Inc.",
        sector="Cloud Software",
        market_cap=245.8,
        price=250.75,
        pe_ratio=125.3,
        ps_ratio=7.2,
        pb_ratio=5.1,
        ev_ebitda=42.5,
        revenue_growth=11.2,
        earnings_growth=8.5,
        sentiment_score=0.45,
        sentiment_trend="down",
        management_guidance="neutral",
        volume=7500000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="NFLX",
        name="Netflix Inc.",
        sector="Streaming",
        market_cap=185.4,
        price=425.80,
        pe_ratio=38.5,
        ps_ratio=5.9,
        pb_ratio=12.4,
        ev_ebitda=22.8,
        revenue_growth=6.7,
        earnings_growth=20.4,
        sentiment_score=0.52,
        sentiment_trend="stable",
        management_guidance="positive",
        volume=4200000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="INTC",
        name="Intel Corporation",
        sector="Semiconductors",
        market_cap=125.3,
        price=29.50,
        pe_ratio=15.2,
        ps_ratio=2.1,
        pb_ratio=1.8,
        ev_ebitda=8.5,
        revenue_growth=-8.2,
        earnings_growth=-45.3,
        sentiment_score=0.15,
        sentiment_trend="down",
        management_guidance="negative",
        volume=35000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="AMD",
        name="Advanced Micro Devices",
        sector="Semiconductors",
        market_cap=185.7,
        price=115.25,
        pe_ratio=185.5,
        ps_ratio=8.5,
        pb_ratio=3.2,
        ev_ebitda=52.3,
        revenue_growth=16.2,
        earnings_growth=-25.4,
        sentiment_score=0.62,
        sentiment_trend="stable",
        management_guidance="neutral",
        volume=52000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="PYPL",
        name="PayPal Holdings",
        sector="FinTech",
        market_cap=68.5,
        price=62.30,
        pe_ratio=18.5,
        ps_ratio=2.4,
        pb_ratio=3.8,
        ev_ebitda=12.5,
        revenue_growth=8.5,
        earnings_growth=22.5,
        sentiment_score=0.42,
        sentiment_trend="up",
        management_guidance="positive",
        volume=12000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="SHOP",
        name="Shopify Inc.",
        sector="E-Commerce Platform",
        market_cap=95.2,
        price=75.50,
        pe_ratio=None,  # Currently unprofitable
        ps_ratio=8.2,
        pb_ratio=7.5,
        ev_ebitda=None,
        revenue_growth=25.2,
        earnings_growth=-85.5,
        sentiment_score=0.58,
        sentiment_trend="up",
        management_guidance="positive",
        volume=8500000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="SQ",
        name="Block Inc.",
        sector="FinTech",
        market_cap=42.8,
        price=68.75,
        pe_ratio=None,
        ps_ratio=1.8,
        pb_ratio=2.1,
        ev_ebitda=None,
        revenue_growth=24.5,
        earnings_growth=-125.3,
        sentiment_score=0.38,
        sentiment_trend="stable",
        management_guidance="neutral",
        volume=14000000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="SPOT",
        name="Spotify Technology",
        sector="Audio Streaming",
        market_cap=52.3,
        price=275.40,
        pe_ratio=None,
        ps_ratio=3.8,
        pb_ratio=18.5,
        ev_ebitda=None,
        revenue_growth=16.1,
        earnings_growth=-45.2,
        sentiment_score=0.48,
        sentiment_trend="stable",
        management_guidance="neutral",
        volume=2800000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="SNOW",
        name="Snowflake Inc.",
        sector="Cloud Software",
        market_cap=48.5,
        price=155.25,
        pe_ratio=None,
        ps_ratio=15.2,
        pb_ratio=8.7,
        ev_ebitda=None,
        revenue_growth=38.2,
        earnings_growth=-25.8,
        sentiment_score=0.65,
        sentiment_trend="up",
        management_guidance="positive",
        volume=5200000,
        last_updated=datetime.now().isoformat()
    ),
    Stock(
        ticker="ZM",
        name="Zoom Video Communications",
        sector="Video Conferencing",
        market_cap=22.4,
        price=72.80,
        pe_ratio=25.4,
        ps_ratio=5.1,
        pb_ratio=4.2,
        ev_ebitda=18.5,
        revenue_growth=3.2,
        earnings_growth=-8.5,
        sentiment_score=0.35,
        sentiment_trend="down",
        management_guidance="neutral",
        volume=6800000,
        last_updated=datetime.now().isoformat()
    ),
]

def get_all_stocks():
    """Get all stocks"""
    return MOCK_STOCKS

def get_stock_by_ticker(ticker):
    """Get stock by ticker symbol"""
    for stock in MOCK_STOCKS:
        if stock.ticker == ticker:
            return stock
    return None

def get_sectors():
    """Get unique sectors"""
    return list(set(stock.sector for stock in MOCK_STOCKS))

def filter_stocks(filters):
    """Filter stocks based on criteria"""
    filtered = MOCK_STOCKS.copy()

    if filters.get('min_market_cap'):
        filtered = [s for s in filtered if s.market_cap >= filters['min_market_cap']]

    if filters.get('max_market_cap'):
        filtered = [s for s in filtered if s.market_cap <= filters['max_market_cap']]

    if filters.get('min_pe_ratio'):
        filtered = [s for s in filtered if s.pe_ratio and s.pe_ratio >= filters['min_pe_ratio']]

    if filters.get('max_pe_ratio'):
        filtered = [s for s in filtered if s.pe_ratio and s.pe_ratio <= filters['max_pe_ratio']]

    if filters.get('min_ps_ratio'):
        filtered = [s for s in filtered if s.ps_ratio and s.ps_ratio >= filters['min_ps_ratio']]

    if filters.get('max_ps_ratio'):
        filtered = [s for s in filtered if s.ps_ratio and s.ps_ratio <= filters['max_ps_ratio']]

    if filters.get('min_revenue_growth'):
        filtered = [s for s in filtered if s.revenue_growth >= filters['min_revenue_growth']]

    if filters.get('min_sentiment_score'):
        filtered = [s for s in filtered if s.sentiment_score >= filters['min_sentiment_score']]

    if filters.get('sectors') and len(filters['sectors']) > 0:
        filtered = [s for s in filtered if s.sector in filters['sectors']]

    if filters.get('management_guidance'):
        filtered = [s for s in filtered if s.management_guidance == filters['management_guidance']]

    return filtered
