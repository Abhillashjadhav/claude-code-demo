# claude-code-demo

## Catalog Read API 2.0 - MVP Demo

This is a **requirements validation harness** and **product demo** for the Catalog Read API 2.0. It simulates the read parity behaviors described in the PRD using a minimal Flask service with sample data.

**Note:** This demo validates *read* behaviors only and mirrors GraphQL intents via REST endpoints. Actual schema, federation, authentication, SLAs, and ID Mapper integration are explicitly out-of-scope for this demo.

## PRD Index

For complete requirements and specifications, see:
- [PRD Index](docs/prds/README.md)
- [Catalog Read API 2.0 PRD](docs/prds/2025-11-catalog-read-api-2.0.md)

## Quick Start

### 1. Set up virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -U pip flask pytest
```

### 3. Run the API server

```bash
export FLASK_APP=src/app.py
flask run --host=127.0.0.1 --port=8001
```

The server will start at `http://127.0.0.1:8001`

### 4. Run tests

```bash
pytest -q
```

## API Endpoints

### Health Check

```bash
curl -s http://127.0.0.1:8001/health
```

**Response:**
```json
{
  "status": "ok"
}
```

### Get Single Product

Retrieve a product by MPLVID (MarketplaceListingVariantID).

```bash
curl -s "http://127.0.0.1:8001/v2/product?mplvid=MPLV-12345&market=US"
```

**Query Parameters:**
- `mplvid` (required): MarketplaceListingVariantID
- `market` (optional): Market context (e.g., US, CA)

**Response Fields:**
- Identifiers: `mplvid`, `mplid`, `supplierPartId`, `legacyIds`
- Core Info: `name`, `description`, `classId`, `className`, `marketContext`
- Status: `statusSummary`, `pipelineStatus`, `statusDetails`
- Option Grouping: `variantGroupId`, `variantAttributes`
- Components: `productType`, `components[]` (for COMPOSITE/KIT types)
- Media: `imagery[]`, `videos[]`, `documents[]`

**Example - Product with Barriers:**
```bash
curl -s "http://127.0.0.1:8001/v2/product?mplvid=MPLV-54321"
```

**Example - Composite Product:**
```bash
curl -s "http://127.0.0.1:8001/v2/product?mplvid=MPLV-99999"
```

### Get Variant Group

Retrieve all variants in a variant group.

```bash
curl -s "http://127.0.0.1:8001/v2/group?variantGroupId=VG-1001&market=US"
```

**Query Parameters:**
- `variantGroupId` (required): Variant group identifier
- `market` (optional): Market context filter

**Response Fields:**
- Group metadata: `variantGroupId`, `mplid`, `marketContext`
- Options: `optionCategories[]` with category definitions
- Variants: `variants[]` with lightweight variant data
- Metadata: `groupingMetadata` with modification history

### List Products

List and filter products across the catalog.

```bash
curl -s "http://127.0.0.1:8001/v2/products?market=US&hasBarriers=true"
```

**Query Parameters (all optional):**
- `market`: Filter by market context
- `classId`: Filter by product class ID
- `productType`: Filter by type (SIMPLE, COMPOSITE, KIT)
- `hasBarriers`: Filter by barrier presence (true/false)
- `lastUpdatedAfter`: Filter by update timestamp (ISO 8601 format)

**Example - Find products updated recently:**
```bash
curl -s "http://127.0.0.1:8001/v2/products?lastUpdatedAfter=2025-11-01T00:00:00Z"
```

**Example - Find composite products:**
```bash
curl -s "http://127.0.0.1:8001/v2/products?productType=COMPOSITE"
```

**Example - Find products with barriers in US market:**
```bash
curl -s "http://127.0.0.1:8001/v2/products?market=US&hasBarriers=true"
```

## Sample Data

The demo includes realistic sample data in `/data`:

- **products.json**: 7 products demonstrating:
  - Variant groups (Office Chair in 3 colors)
  - Products with barriers and validation errors
  - Pipeline status (sanitized step view)
  - Legacy ID mapping
  - Composite/Kit product structure
  - Different market contexts (US, CA)
  - Media with moderation status

- **groups.json**: 2 variant groups showing:
  - Option categories and values
  - Variant metadata and rankings
  - Grouping modification history

## Key Features Demonstrated

✓ **CDF 2.0 Identifiers**: MPLVID, MPLID, ChoiceID
✓ **Legacy ID Migration**: Backward-compatible legacy identifiers
✓ **Option Grouping**: Variant families with option metadata
✓ **Pipeline Status**: Sanitized processing steps with timestamps
✓ **Barriers & Validations**: Actionable error codes with remediation links
✓ **Composites/Kits**: Component relationships with cross-supplier redaction
✓ **Market Context**: Multi-market product availability
✓ **Media Management**: Signed URLs with moderation status

## Architecture

```
/
├── data/
│   ├── products.json      # Sample product catalog
│   └── groups.json        # Sample variant groups
├── src/
│   ├── app.py            # Flask API endpoints
│   └── data.py           # Data loader and query logic
├── tests/
│   └── test_app.py       # Comprehensive test suite
└── docs/
    └── prds/
        ├── README.md                           # PRD index
        └── 2025-11-catalog-read-api-2.0.md    # Full PRD
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_app.py::test_get_product_success
```

### Adding Sample Data

Edit `data/products.json` or `data/groups.json` to add more sample products or variant groups. The server will automatically load the updated data on restart.

## Deploy to Production (Free Tier)

This demo can be deployed to a public URL for stakeholder testing using free tier services.

### Option 1: Deploy to Render.com (Recommended)

1. **Sign up for Render.com** (free tier available)
   - Go to https://render.com and sign up

2. **Connect your GitHub repository**
   - In Render dashboard, click "New +" → "Web Service"
   - Connect your GitHub account
   - Select the `claude-code-demo` repository

3. **Configure the deployment**
   - Render will auto-detect the `render.yaml` configuration
   - Or manually configure:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `cd src && PYTHONPATH=/opt/render/project gunicorn app:app --bind 0.0.0.0:$PORT`
     - **Environment Variables:** `FLASK_ENV=production`

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app
   - You'll get a public URL like: `https://catalog-read-api-demo.onrender.com`

5. **Share the URL**
   - The dashboard will be at: `https://your-app.onrender.com/`
   - The API will be at: `https://your-app.onrender.com/v2/product?mplvid=MPLV-12345`

**Note:** Free tier apps on Render spin down after inactivity and may take 30-60 seconds to wake up on first request.

### Option 2: Deploy to Railway.app

1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and deploy
5. Add environment variable: `FLASK_ENV=production`

### Option 3: Deploy to Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login and launch
fly auth login
fly launch

# Deploy
fly deploy
```

## Production Considerations

This demo is for **requirements validation** and **internal product review only**. For production deployment, the following must be implemented:

- GraphQL schema and federation layer (vs. REST)
- OAuth2 authentication and authorization
- ID Mapper service integration
- Real-time pipeline/barrier data sources
- Performance optimization (caching, pagination)
- Rate limiting and monitoring
- Comprehensive error handling
- API documentation (OpenAPI/GraphQL schema)

## Support

For questions about the PRD or requirements, see:
- [Catalog Read API 2.0 PRD](docs/prds/2025-11-catalog-read-api-2.0.md)

For issues with this demo:
- Check that data files exist in `/data`
- Verify virtual environment is activated
- Ensure Flask is running on port 8001
- Review test output for detailed error messages
