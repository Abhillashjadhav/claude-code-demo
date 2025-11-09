# Quick Start Guide

Get the NASDAQ Tech Screener up and running in 5 minutes!

## Prerequisites

- Python 3.7+
- A modern web browser

## Installation (2 minutes)

1. **Install dependencies**:
```bash
pip install -r Requirements.txt
```

## Running the Application (1 minute)

### Step 1: Start the Backend

Open a terminal and run:
```bash
cd src
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### Step 2: Open the Frontend

**Option A - Direct File Open** (Easiest)
- Open `frontend/index.html` in your browser

**Option B - Local Web Server** (Recommended)
```bash
# In a new terminal
cd frontend
python -m http.server 8000
```
Then visit: http://localhost:8000

## That's It!

You should now see the NASDAQ Tech Screener application with 18 tech stocks ready to filter and analyze.

## Quick Tips

1. **Try filtering**: Set max P/E to 30 and min revenue growth to 10%, then click "Apply Filters"
2. **Add to watchlist**: Click the star icon next to any stock
3. **View details**: Click on any ticker symbol to see full metrics
4. **Export data**: Click "Export CSV" to download your filtered results
5. **Dark mode**: Click the moon icon in the header

## Running Tests

```bash
cd src
pytest
```

## Troubleshooting

**Frontend shows "Error loading stocks"**
- Make sure the backend is running on port 5000
- Check that flask-cors is installed: `pip install flask-cors`

**Import errors when starting backend**
- Ensure you're in the `src` directory when running `python app.py`
- Verify all dependencies are installed: `pip install -r Requirements.txt`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize the stock data in `src/data.py`
- Modify the UI colors in `frontend/css/styles.css`
- Add your own filters and features

## Support

Having issues? Check the [README.md](README.md) for more detailed setup instructions.
