import json
import pytest
from src.app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ============================================================================
# Health Check Tests
# ============================================================================

def test_health_endpoint(client):
    """Test that health endpoint returns 200 and correct status"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}


# ============================================================================
# Get All Stocks Tests
# ============================================================================

def test_get_all_stocks_returns_200(client):
    """Test that /api/stocks returns 200 status"""
    response = client.get('/api/stocks')
    assert response.status_code == 200


def test_get_all_stocks_returns_list(client):
    """Test that /api/stocks returns a list"""
    response = client.get('/api/stocks')
    assert isinstance(response.json, list)


def test_get_all_stocks_count(client):
    """Test that /api/stocks returns exactly 18 stocks"""
    response = client.get('/api/stocks')
    assert len(response.json) == 18


def test_get_all_stocks_structure(client):
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


# ============================================================================
# Get Stock by Ticker Tests
# ============================================================================

def test_get_stock_by_ticker_success(client):
    """Test retrieving a valid stock by ticker"""
    response = client.get('/api/stocks/AAPL')
    assert response.status_code == 200
    assert response.json['ticker'] == 'AAPL'
    assert response.json['name'] == 'Apple Inc.'


def test_get_stock_by_ticker_case_insensitive(client):
    """Test that ticker lookup is case-insensitive"""
    response = client.get('/api/stocks/aapl')
    assert response.status_code == 200
    assert response.json['ticker'] == 'AAPL'


def test_get_stock_by_ticker_not_found(client):
    """Test 404 for non-existent ticker"""
    response = client.get('/api/stocks/INVALID')
    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == 'Stock not found'


# ============================================================================
# Get Sectors Tests
# ============================================================================

def test_get_sectors_returns_200(client):
    """Test that /api/sectors returns 200"""
    response = client.get('/api/sectors')
    assert response.status_code == 200


def test_get_sectors_returns_list(client):
    """Test that /api/sectors returns a list"""
    response = client.get('/api/sectors')
    assert isinstance(response.json, list)


def test_get_sectors_unique(client):
    """Test that sectors list contains unique values"""
    response = client.get('/api/sectors')
    sectors = response.json
    assert len(sectors) == len(set(sectors))


def test_get_sectors_contains_expected(client):
    """Test that sectors list contains known sectors"""
    response = client.get('/api/sectors')
    sectors = response.json
    expected_sectors = ['Software', 'Semiconductors', 'Consumer Electronics']
    for sector in expected_sectors:
        assert sector in sectors


# ============================================================================
# Screen Stocks - Basic Filtering Tests
# ============================================================================

def test_screen_stocks_no_filters(client):
    """Test screening with no filters returns all stocks"""
    response = client.post('/api/screen', json={})
    assert response.status_code == 200
    assert len(response.json) == 18


def test_screen_stocks_empty_body(client):
    """Test screening with empty JSON body returns all stocks"""
    response = client.post('/api/screen',
                          data='{}',
                          content_type='application/json')
    assert response.status_code == 200
    assert len(response.json) == 18


def test_filter_by_min_market_cap(client):
    """Test filtering by minimum market cap"""
    response = client.post('/api/screen', json={'min_market_cap': 1000})
    assert response.status_code == 200
    # All returned stocks should have market_cap >= 1000
    for stock in response.json:
        assert stock['market_cap'] >= 1000


def test_filter_by_max_market_cap(client):
    """Test filtering by maximum market cap"""
    response = client.post('/api/screen', json={'max_market_cap': 100})
    assert response.status_code == 200
    # All returned stocks should have market_cap <= 100
    for stock in response.json:
        assert stock['market_cap'] <= 100


def test_filter_by_market_cap_range(client):
    """Test filtering by market cap range"""
    response = client.post('/api/screen', json={
        'min_market_cap': 100,
        'max_market_cap': 500
    })
    assert response.status_code == 200
    for stock in response.json:
        assert 100 <= stock['market_cap'] <= 500


# ============================================================================
# Screen Stocks - P/E and P/S Filtering Tests
# ============================================================================

def test_filter_by_min_pe_ratio(client):
    """Test filtering by minimum P/E ratio"""
    response = client.post('/api/screen', json={'min_pe_ratio': 30})
    assert response.status_code == 200
    # All returned stocks with pe_ratio should have value >= 30
    for stock in response.json:
        if stock['pe_ratio'] is not None:
            assert stock['pe_ratio'] >= 30


def test_filter_by_max_pe_ratio(client):
    """Test filtering by maximum P/E ratio"""
    response = client.post('/api/screen', json={'max_pe_ratio': 25})
    assert response.status_code == 200
    for stock in response.json:
        if stock['pe_ratio'] is not None:
            assert stock['pe_ratio'] <= 25


def test_filter_excludes_null_pe_ratios(client):
    """Test that min/max PE filters exclude stocks with null PE"""
    response = client.post('/api/screen', json={'min_pe_ratio': 10})
    assert response.status_code == 200
    # No stock with null pe_ratio should be in results
    for stock in response.json:
        assert stock['pe_ratio'] is not None


def test_filter_by_ps_ratio_range(client):
    """Test filtering by P/S ratio range"""
    response = client.post('/api/screen', json={
        'min_ps_ratio': 5,
        'max_ps_ratio': 10
    })
    assert response.status_code == 200
    for stock in response.json:
        if stock['ps_ratio'] is not None:
            assert 5 <= stock['ps_ratio'] <= 10


# ============================================================================
# Screen Stocks - Growth and Sentiment Tests
# ============================================================================

def test_filter_by_min_revenue_growth(client):
    """Test filtering by minimum revenue growth"""
    response = client.post('/api/screen', json={'min_revenue_growth': 15})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['revenue_growth'] >= 15


def test_filter_by_negative_revenue_growth(client):
    """Test filtering allows negative revenue growth values"""
    response = client.post('/api/screen', json={'min_revenue_growth': -10})
    assert response.status_code == 200
    # Should return stocks with revenue_growth >= -10
    for stock in response.json:
        assert stock['revenue_growth'] >= -10


def test_filter_by_min_sentiment(client):
    """Test filtering by minimum sentiment score"""
    response = client.post('/api/screen', json={'min_sentiment_score': 0.6})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['sentiment_score'] >= 0.6


def test_filter_by_sentiment_range(client):
    """Test sentiment filtering with valid range"""
    response = client.post('/api/screen', json={'min_sentiment_score': 0.5})
    assert response.status_code == 200
    for stock in response.json:
        assert -1 <= stock['sentiment_score'] <= 1
        assert stock['sentiment_score'] >= 0.5


# ============================================================================
# Screen Stocks - Sector and Guidance Tests
# ============================================================================

def test_filter_by_single_sector(client):
    """Test filtering by single sector"""
    response = client.post('/api/screen', json={'sectors': ['Software']})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['sector'] == 'Software'


def test_filter_by_multiple_sectors(client):
    """Test filtering by multiple sectors"""
    sectors = ['Software', 'Semiconductors']
    response = client.post('/api/screen', json={'sectors': sectors})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['sector'] in sectors


def test_filter_by_empty_sectors_list(client):
    """Test that empty sectors list returns all stocks"""
    response = client.post('/api/screen', json={'sectors': []})
    assert response.status_code == 200
    assert len(response.json) == 18


def test_filter_by_management_guidance_positive(client):
    """Test filtering by positive management guidance"""
    response = client.post('/api/screen', json={'management_guidance': 'positive'})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['management_guidance'] == 'positive'


def test_filter_by_management_guidance_neutral(client):
    """Test filtering by neutral management guidance"""
    response = client.post('/api/screen', json={'management_guidance': 'neutral'})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['management_guidance'] == 'neutral'


def test_filter_by_management_guidance_negative(client):
    """Test filtering by negative management guidance"""
    response = client.post('/api/screen', json={'management_guidance': 'negative'})
    assert response.status_code == 200
    for stock in response.json:
        assert stock['management_guidance'] == 'negative'


# ============================================================================
# Screen Stocks - Complex Filtering Tests
# ============================================================================

def test_filter_multiple_criteria(client):
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


def test_filter_no_matches(client):
    """Test filtering that returns zero results"""
    filters = {
        'min_market_cap': 10000,  # No stock has this market cap
    }
    response = client.post('/api/screen', json=filters)
    assert response.status_code == 200
    assert len(response.json) == 0
    assert response.json == []


def test_filter_invalid_range(client):
    """Test filtering with min > max returns empty results"""
    filters = {
        'min_market_cap': 1000,
        'max_market_cap': 100  # Invalid: min > max
    }
    response = client.post('/api/screen', json=filters)
    assert response.status_code == 200
    assert len(response.json) == 0


# ============================================================================
# Get Statistics Tests
# ============================================================================

def test_get_stats_returns_200(client):
    """Test that /api/stats returns 200"""
    response = client.get('/api/stats')
    assert response.status_code == 200


def test_get_stats_structure(client):
    """Test that stats response has correct structure"""
    response = client.get('/api/stats')
    data = response.json
    assert 'total_stocks' in data
    assert 'average_pe' in data
    assert 'average_sentiment' in data
    assert 'guidance_breakdown' in data


def test_get_stats_total_stocks(client):
    """Test that total_stocks is correct"""
    response = client.get('/api/stats')
    assert response.json['total_stocks'] == 18


def test_get_stats_average_pe_valid(client):
    """Test that average_pe is a valid number"""
    response = client.get('/api/stats')
    avg_pe = response.json['average_pe']
    assert isinstance(avg_pe, (int, float))
    assert avg_pe > 0


def test_get_stats_average_sentiment_range(client):
    """Test that average_sentiment is within valid range"""
    response = client.get('/api/stats')
    avg_sentiment = response.json['average_sentiment']
    assert -1 <= avg_sentiment <= 1


def test_get_stats_guidance_breakdown(client):
    """Test guidance breakdown structure and totals"""
    response = client.get('/api/stats')
    breakdown = response.json['guidance_breakdown']
    assert 'positive' in breakdown
    assert 'neutral' in breakdown
    assert 'negative' in breakdown
    # Total should equal total stocks
    total = breakdown['positive'] + breakdown['neutral'] + breakdown['negative']
    assert total == 18
