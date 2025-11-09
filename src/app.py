from flask import Flask, request, jsonify
from flask_cors import CORS
from src.data import get_all_stocks, get_stock_by_ticker, get_sectors, filter_stocks

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

@app.route("/api/stocks", methods=["GET"])
def get_stocks():
    """Get all stocks"""
    stocks = get_all_stocks()
    return jsonify([stock.to_dict() for stock in stocks]), 200

@app.route("/api/stocks/<ticker>", methods=["GET"])
def get_stock(ticker):
    """Get stock by ticker"""
    stock = get_stock_by_ticker(ticker.upper())
    if stock:
        return jsonify(stock.to_dict()), 200
    return jsonify(error="Stock not found"), 404

@app.route("/api/sectors", methods=["GET"])
def sectors():
    """Get all unique sectors"""
    return jsonify(get_sectors()), 200

@app.route("/api/screen", methods=["POST"])
def screen_stocks():
    """Screen stocks based on filter criteria"""
    filters = request.json or {}
    filtered_stocks = filter_stocks(filters)
    return jsonify([stock.to_dict() for stock in filtered_stocks]), 200

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get overall market statistics"""
    stocks = get_all_stocks()

    total_stocks = len(stocks)
    avg_pe = sum(s.pe_ratio for s in stocks if s.pe_ratio) / len([s for s in stocks if s.pe_ratio])
    avg_sentiment = sum(s.sentiment_score for s in stocks) / total_stocks

    positive_guidance = len([s for s in stocks if s.management_guidance == "positive"])
    neutral_guidance = len([s for s in stocks if s.management_guidance == "neutral"])
    negative_guidance = len([s for s in stocks if s.management_guidance == "negative"])

    return jsonify({
        "total_stocks": total_stocks,
        "average_pe": round(avg_pe, 2),
        "average_sentiment": round(avg_sentiment, 2),
        "guidance_breakdown": {
            "positive": positive_guidance,
            "neutral": neutral_guidance,
            "negative": negative_guidance
        }
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
