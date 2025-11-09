import json
from src.app import app

def client():
    return app.test_client()

def test_health():
    c = client()
    resp = c.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_get_all_stocks():
    """Test getting all stocks"""
    c = client()
    resp = c.get("/api/stocks")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "ticker" in data[0]
    assert "name" in data[0]

def test_get_stock_by_ticker():
    """Test getting a specific stock by ticker"""
    c = client()
    resp = c.get("/api/stocks/AAPL")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ticker"] == "AAPL"
    assert data["name"] == "Apple Inc."

def test_get_nonexistent_stock():
    """Test getting a stock that doesn't exist"""
    c = client()
    resp = c.get("/api/stocks/INVALID")
    assert resp.status_code == 404

def test_get_sectors():
    """Test getting all sectors"""
    c = client()
    resp = c.get("/api/sectors")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_screen_stocks_no_filters():
    """Test screening with no filters"""
    c = client()
    resp = c.post("/api/screen", json={})
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_screen_stocks_with_market_cap_filter():
    """Test screening with market cap filter"""
    c = client()
    resp = c.post("/api/screen", json={"min_market_cap": 1000})
    assert resp.status_code == 200
    data = resp.get_json()
    for stock in data:
        assert stock["market_cap"] >= 1000

def test_screen_stocks_with_sector_filter():
    """Test screening with sector filter"""
    c = client()
    resp = c.post("/api/screen", json={"sectors": ["Software"]})
    assert resp.status_code == 200
    data = resp.get_json()
    for stock in data:
        assert stock["sector"] == "Software"

def test_get_stats():
    """Test getting market statistics"""
    c = client()
    resp = c.get("/api/stats")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "total_stocks" in data
    assert "average_pe" in data
    assert "average_sentiment" in data
    assert data["total_stocks"] > 0
