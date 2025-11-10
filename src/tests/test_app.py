import json
import pytest
from src.app import app


@pytest.fixture
def client():
    """Flask test client fixture."""
    return app.test_client()


def test_health(client):
    """Test health endpoint returns ok status."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_screener_no_filters(client):
    """Test screener endpoint with no filters returns all stocks."""
    resp = client.get("/screener")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_screener_with_pe_filter(client):
    """Test screener endpoint with P/E filter."""
    resp = client.get("/screener?pe_max=30")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    # All returned stocks should have PE <= 30
    for stock in data:
        if stock['pe'] is not None:
            assert stock['pe'] <= 30


def test_screener_with_ps_filter(client):
    """Test screener endpoint with P/S filter."""
    resp = client.get("/screener?ps_max=10")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    # All returned stocks should have PS <= 10
    for stock in data:
        if stock['ps'] is not None:
            assert stock['ps'] <= 10


def test_screener_with_sentiment_filter(client):
    """Test screener endpoint with sentiment filter."""
    resp = client.get("/screener?sentiment_min=75")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    # All returned stocks should have sentiment >= 75
    for stock in data:
        if stock['sentiment'] is not None:
            assert stock['sentiment'] >= 75


def test_screener_with_multiple_filters(client):
    """Test screener endpoint with multiple filters."""
    resp = client.get("/screener?pe_max=30&ps_max=10&sentiment_min=70")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    # All returned stocks should meet all criteria
    for stock in data:
        if stock['pe'] is not None:
            assert stock['pe'] <= 30
        if stock['ps'] is not None:
            assert stock['ps'] <= 10
        if stock['sentiment'] is not None:
            assert stock['sentiment'] >= 70


def test_screener_invalid_pe(client):
    """Test screener endpoint with invalid P/E parameter."""
    resp = client.get("/screener?pe_max=invalid")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_screener_negative_pe(client):
    """Test screener endpoint with negative P/E parameter."""
    resp = client.get("/screener?pe_max=-10")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_screener_invalid_sentiment(client):
    """Test screener endpoint with out of range sentiment."""
    resp = client.get("/screener?sentiment_min=150")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_get_stock_valid(client):
    """Test getting a valid stock by ticker."""
    resp = client.get("/stocks/AAPL")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ticker"] == "AAPL"
    assert "name" in data
    assert "pe" in data
    assert "ps" in data
    assert "sentiment" in data


def test_get_stock_case_insensitive(client):
    """Test getting a stock with lowercase ticker."""
    resp = client.get("/stocks/aapl")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ticker"] == "AAPL"


def test_get_stock_not_found(client):
    """Test getting a non-existent stock."""
    resp = client.get("/stocks/INVALID")
    assert resp.status_code == 404
    assert "error" in resp.get_json()


def test_invalid_endpoint(client):
    """Test accessing an invalid endpoint."""
    resp = client.get("/invalid")
    assert resp.status_code == 404
    assert "error" in resp.get_json()
