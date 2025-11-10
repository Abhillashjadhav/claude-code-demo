"""
Data loader module for stock data.
"""
import csv
import os
from typing import List, Dict, Optional


def load_stocks(csv_path: str = None) -> List[Dict]:
    """
    Load stock data from CSV file.

    Args:
        csv_path: Path to CSV file. If None, uses default path.

    Returns:
        List of dictionaries containing stock data.
    """
    if csv_path is None:
        # Default path relative to project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, 'data', 'sample_stocks.csv')

    stocks = []

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stock = {
                    'ticker': row['ticker'],
                    'name': row['name'],
                    'pe': _parse_float(row['pe']),
                    'ps': _parse_float(row['ps']),
                    'sentiment': _parse_float(row['sentiment'])
                }
                stocks.append(stock)
    except FileNotFoundError:
        raise FileNotFoundError(f"Stock data file not found: {csv_path}")
    except Exception as e:
        raise Exception(f"Error loading stock data: {str(e)}")

    return stocks


def _parse_float(value: str) -> Optional[float]:
    """
    Parse string to float, handling N/A values.

    Args:
        value: String value to parse.

    Returns:
        Float value or None if N/A.
    """
    value = value.strip()
    if value.upper() in ('N/A', 'NA', ''):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def get_stock_by_ticker(ticker: str, stocks: List[Dict]) -> Optional[Dict]:
    """
    Find a stock by ticker symbol.

    Args:
        ticker: Stock ticker symbol (case-insensitive).
        stocks: List of stock dictionaries.

    Returns:
        Stock dictionary or None if not found.
    """
    ticker_upper = ticker.upper()
    for stock in stocks:
        if stock['ticker'].upper() == ticker_upper:
            return stock
    return None


def filter_stocks(
    stocks: List[Dict],
    pe_max: Optional[float] = None,
    ps_max: Optional[float] = None,
    sentiment_min: Optional[float] = None
) -> List[Dict]:
    """
    Filter stocks based on criteria.

    Args:
        stocks: List of stock dictionaries.
        pe_max: Maximum P/E ratio (inclusive).
        ps_max: Maximum P/S ratio (inclusive).
        sentiment_min: Minimum sentiment score (inclusive).

    Returns:
        Filtered list of stocks.
    """
    filtered = []

    for stock in stocks:
        # Apply filters
        if pe_max is not None:
            # Skip if stock has no P/E ratio or it exceeds max
            if stock['pe'] is None or stock['pe'] > pe_max:
                continue

        if ps_max is not None:
            # Skip if stock has no P/S ratio or it exceeds max
            if stock['ps'] is None or stock['ps'] > ps_max:
                continue

        if sentiment_min is not None:
            # Skip if stock has no sentiment or it's below min
            if stock['sentiment'] is None or stock['sentiment'] < sentiment_min:
                continue

        filtered.append(stock)

    return filtered
