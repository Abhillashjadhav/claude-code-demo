from flask import Flask, jsonify, request, render_template
import csv
import os
from functools import lru_cache

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(APP_ROOT, "..", "data"))
CSV_ALL = os.path.join(DATA_DIR, "all_nasdaq.csv")
CSV_SAMPLE = os.path.join(DATA_DIR, "sample_stocks.csv")

app = Flask(__name__, template_folder="templates", static_folder="static")

# --------------------- Data loading ---------------------

def _to_float(v):
    try:
        return float(v)
    except Exception:
        return None

def _csv_path():
    return CSV_ALL if os.path.exists(CSV_ALL) else CSV_SAMPLE

@lru_cache(maxsize=1)
def _load_rows_cached(csv_path):
    rows = []
    if not os.path.exists(csv_path):
        return rows
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "ticker": (r.get("ticker") or "").strip(),
                "name": r.get("name"),
                "pe": _to_float(r.get("pe")),
                "ps": _to_float(r.get("ps")),
                "sentiment": _to_float(r.get("sentiment")),
                "lastUpdated": r.get("lastUpdated") or None,
            })
    return rows

def load_rows():
    return _load_rows_cached(_csv_path())

def reload_data():
    _load_rows_cached.cache_clear()  # invalidate
    # prime cache
    _ = load_rows()

# --------------------- UI ---------------------

@app.route("/")
def home():
    return render_template("index.html")

# --------------------- API ---------------------

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/admin/reload", methods=["POST"])
def admin_reload():
    reload_data()
    return jsonify({"ok": True, "count": len(load_rows())})

@app.route("/screener")
def screener():
    rows = load_rows()

    # filters (optional)
    pe_max = request.args.get("pe_max", type=float)
    ps_max = request.args.get("ps_max", type=float)
    sentiment_min = request.args.get("sentiment_min", type=float)

    # sorting
    sort_by = request.args.get("sort_by", default="ticker")  # ticker|pe|ps|sentiment
    sort_dir = request.args.get("sort_dir", default="asc")    # asc|desc

    # pagination
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=50, type=int)
    page = max(1, page)
    page_size = min(max(1, page_size), 200)  # cap page size

    # filter
    def keep(r):
        if pe_max is not None and (r["pe"] is None or r["pe"] > pe_max): return False
        if ps_max is not None and (r["ps"] is None or r["ps"] > ps_max): return False
        if sentiment_min is not None and (r["sentiment"] is None or r["sentiment"] < sentiment_min): return False
        return True

    filtered = [r for r in rows if keep(r)]

    # sort
    key_map = {
        "ticker": lambda x: (x["ticker"] or ""),
        "pe": lambda x: (x["pe"] is None, x["pe"] or 0.0),
        "ps": lambda x: (x["ps"] is None, x["ps"] or 0.0),
        "sentiment": lambda x: (x["sentiment"] is None, x["sentiment"] or 0.0),
    }
    key_fn = key_map.get(sort_by, key_map["ticker"])
    filtered.sort(key=key_fn, reverse=(sort_dir == "desc"))

    # paginate
    total = len(filtered)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = filtered[start:end]
    total_pages = (total + page_size - 1) // page_size if page_size else 1

    return jsonify({
        "items": page_items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages
    })

@app.route("/stocks/<ticker>")
def stock_detail(ticker):
    rows = load_rows()
    for r in rows:
        if r["ticker"] and r["ticker"].upper() == ticker.upper():
            return jsonify(r)
    return jsonify({"error": "not_found", "message": f"Ticker {ticker} not found"}), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
