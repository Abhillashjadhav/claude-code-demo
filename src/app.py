"""
Flask application for NASDAQ tech valuation screener.
"""
from flask import Flask, jsonify, request
from typing import Dict, Any
from src import data


app = Flask(__name__)

# Load stock data on startup
try:
    STOCKS = data.load_stocks()
except Exception as e:
    print(f"Error loading stock data: {e}")
    STOCKS = []


@app.route('/health', methods=['GET'])
def health() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        JSON response with status.
    """
    return jsonify({'status': 'ok'})


@app.route('/screener', methods=['GET'])
def screener() -> Any:
    """
    Screener endpoint with optional filters.

    Query Parameters:
        pe_max (float): Maximum P/E ratio
        ps_max (float): Maximum P/S ratio
        sentiment_min (float): Minimum sentiment score

    Returns:
        JSON array of filtered stocks or error message.
    """
    # Parse query parameters
    pe_max = request.args.get('pe_max')
    ps_max = request.args.get('ps_max')
    sentiment_min = request.args.get('sentiment_min')

    # Validate and convert parameters
    try:
        pe_max_val = None
        if pe_max is not None:
            pe_max_val = float(pe_max)
            if pe_max_val <= 0:
                return jsonify({'error': 'pe_max must be positive'}), 400

        ps_max_val = None
        if ps_max is not None:
            ps_max_val = float(ps_max)
            if ps_max_val <= 0:
                return jsonify({'error': 'ps_max must be positive'}), 400

        sentiment_min_val = None
        if sentiment_min is not None:
            sentiment_min_val = float(sentiment_min)
            if sentiment_min_val < 0 or sentiment_min_val > 100:
                return jsonify({'error': 'sentiment_min must be between 0 and 100'}), 400

    except ValueError as e:
        return jsonify({'error': f'Invalid parameter format: {str(e)}'}), 400

    # Filter stocks
    filtered_stocks = data.filter_stocks(
        STOCKS,
        pe_max=pe_max_val,
        ps_max=ps_max_val,
        sentiment_min=sentiment_min_val
    )

    return jsonify(filtered_stocks)


@app.route('/stocks/<ticker>', methods=['GET'])
def get_stock(ticker: str) -> Any:
    """
    Get a single stock by ticker.

    Args:
        ticker: Stock ticker symbol.

    Returns:
        JSON object of stock or 404 error.
    """
    stock = data.get_stock_by_ticker(ticker, STOCKS)

    if stock is None:
        return jsonify({'error': f'Stock not found: {ticker}'}), 404

    return jsonify(stock)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
