#!/usr/bin/env python
"""Demo script to show the stock screener functionality"""

import sys
sys.path.insert(0, 'src')

from data import get_all_stocks, filter_stocks, get_sectors

def print_separator():
    print("\n" + "="*80 + "\n")

def main():
    print("NASDAQ Tech Screener - Demo")
    print_separator()

    # Show all stocks
    all_stocks = get_all_stocks()
    print(f"Total stocks in database: {len(all_stocks)}")
    print("\nSample stocks:")
    for stock in all_stocks[:5]:
        print(f"  {stock.ticker:6} - {stock.name:30} ${stock.price:8.2f}  P/E: {stock.pe_ratio or 'N/A'}")

    print_separator()

    # Show available sectors
    sectors = get_sectors()
    print(f"Available sectors: {', '.join(sectors)}")

    print_separator()

    # Demo filter 1: Undervalued large caps
    print("Filter Example 1: Large caps with low P/E (value stocks)")
    filters = {
        'min_market_cap': 500,
        'max_pe_ratio': 30
    }
    filtered = filter_stocks(filters)
    print(f"Found {len(filtered)} matching stocks:")
    for stock in filtered:
        print(f"  {stock.ticker:6} - {stock.name:30} "
              f"MCap: ${stock.market_cap:6.1f}B  P/E: {stock.pe_ratio:5.1f}")

    print_separator()

    # Demo filter 2: High growth with positive sentiment
    print("Filter Example 2: High growth stocks with positive sentiment")
    filters = {
        'min_revenue_growth': 20,
        'min_sentiment_score': 0.6
    }
    filtered = filter_stocks(filters)
    print(f"Found {len(filtered)} matching stocks:")
    for stock in filtered:
        print(f"  {stock.ticker:6} - {stock.name:30} "
              f"Growth: {stock.revenue_growth:5.1f}%  Sentiment: {stock.sentiment_score:4.2f}")

    print_separator()

    # Demo filter 3: Software sector with positive guidance
    print("Filter Example 3: Software companies with positive management guidance")
    filters = {
        'sectors': ['Software'],
        'management_guidance': 'positive'
    }
    filtered = filter_stocks(filters)
    print(f"Found {len(filtered)} matching stocks:")
    for stock in filtered:
        print(f"  {stock.ticker:6} - {stock.name:30} "
              f"Sector: {stock.sector:20} Guidance: {stock.management_guidance}")

    print_separator()

    # Show summary stats
    print("Summary Statistics:")
    avg_pe = sum(s.pe_ratio for s in all_stocks if s.pe_ratio) / len([s for s in all_stocks if s.pe_ratio])
    avg_sentiment = sum(s.sentiment_score for s in all_stocks) / len(all_stocks)
    positive_count = len([s for s in all_stocks if s.management_guidance == 'positive'])

    print(f"  Average P/E Ratio: {avg_pe:.2f}")
    print(f"  Average Sentiment: {avg_sentiment:.2f}")
    print(f"  Stocks with Positive Guidance: {positive_count}/{len(all_stocks)}")

    print_separator()
    print("Demo complete! Run the web application to interact with the screener.")
    print("\nTo start the backend:  cd src && python app.py")
    print("To open the frontend:  Open frontend/index.html in your browser")

if __name__ == '__main__':
    main()
