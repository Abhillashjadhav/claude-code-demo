"""Tests for Read API 2.0 MVP Demo."""
import pytest
import json
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    """Test the /health endpoint returns 200 and expected status."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"status": "ok"}


def test_get_product_success(client):
    """Test /v2/product returns expected product fields."""
    response = client.get('/v2/product?mplvid=MPLV-12345')
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify key fields are present
    assert data['mplvid'] == 'MPLV-12345'
    assert data['mplid'] == 'MPL-100'
    assert 'name' in data
    assert 'classId' in data
    assert 'marketContext' in data
    assert 'statusSummary' in data
    assert 'pipelineStatus' in data
    assert 'statusDetails' in data
    assert 'legacyIds' in data


def test_get_product_with_market(client):
    """Test /v2/product with market filter."""
    response = client.get('/v2/product?mplvid=MPLV-12345&market=US')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['mplvid'] == 'MPLV-12345'
    assert data['marketContext'] == 'US'


def test_get_product_not_found(client):
    """Test /v2/product returns 404 for unknown MPLVID."""
    response = client.get('/v2/product?mplvid=INVALID-ID')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['code'] == 'NOT_FOUND'


def test_get_product_missing_mplvid(client):
    """Test /v2/product returns 400 when mplvid is missing."""
    response = client.get('/v2/product')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['code'] == 'MISSING_PARAMETER'


def test_get_group_success(client):
    """Test /v2/group returns expected grouping fields."""
    response = client.get('/v2/group?variantGroupId=VG-1001')
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify key fields are present
    assert data['variantGroupId'] == 'VG-1001'
    assert data['mplid'] == 'MPL-100'
    assert 'marketContext' in data
    assert 'optionCategories' in data
    assert 'variants' in data
    assert 'groupingMetadata' in data

    # Verify variants structure
    assert len(data['variants']) >= 1
    variant = data['variants'][0]
    assert 'mplvid' in variant
    assert 'name' in variant
    assert 'optionValues' in variant


def test_get_group_with_market(client):
    """Test /v2/group with market filter."""
    response = client.get('/v2/group?variantGroupId=VG-1001&market=US')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['variantGroupId'] == 'VG-1001'
    assert data['marketContext'] == 'US'


def test_get_group_not_found(client):
    """Test /v2/group returns 404 for unknown variantGroupId."""
    response = client.get('/v2/group?variantGroupId=INVALID-GROUP')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['code'] == 'NOT_FOUND'


def test_get_group_missing_id(client):
    """Test /v2/group returns 400 when variantGroupId is missing."""
    response = client.get('/v2/group')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['code'] == 'MISSING_PARAMETER'


def test_list_products_all(client):
    """Test /v2/products returns list of all products."""
    response = client.get('/v2/products')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'products' in data
    assert 'count' in data
    assert data['count'] > 0
    assert len(data['products']) == data['count']


def test_list_products_by_market(client):
    """Test /v2/products filters by market."""
    response = client.get('/v2/products?market=US')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'products' in data
    # All returned products should have US in marketContext or availableMarkets
    for product in data['products']:
        assert (product['marketContext'] == 'US' or
                'US' in product.get('availableMarkets', []))


def test_list_products_with_barriers(client):
    """Test /v2/products filters by hasBarriers."""
    response = client.get('/v2/products?hasBarriers=true')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'products' in data
    # All returned products should have barriers
    for product in data['products']:
        barrier_reasons = product.get('statusDetails', {}).get('barrierReasons', [])
        assert len(barrier_reasons) > 0


def test_list_products_without_barriers(client):
    """Test /v2/products filters by hasBarriers=false."""
    response = client.get('/v2/products?hasBarriers=false')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'products' in data
    # All returned products should have no barriers
    for product in data['products']:
        barrier_reasons = product.get('statusDetails', {}).get('barrierReasons', [])
        assert len(barrier_reasons) == 0


def test_list_products_by_last_updated(client):
    """Test /v2/products filters by lastUpdatedAfter."""
    response = client.get('/v2/products?lastUpdatedAfter=2025-11-01T00:00:00Z')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'products' in data
    # Products returned should be updated after the cutoff
    # (We should have at least some products from November)
    assert data['count'] > 0


def test_list_products_by_product_type(client):
    """Test /v2/products filters by productType."""
    response = client.get('/v2/products?productType=COMPOSITE')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'products' in data
    # All returned products should be of type COMPOSITE
    for product in data['products']:
        assert product['productType'] == 'COMPOSITE'


def test_list_products_by_class_id(client):
    """Test /v2/products filters by classId."""
    response = client.get('/v2/products?classId=CLS-500')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'products' in data
    # All returned products should have the specified classId
    for product in data['products']:
        assert product['classId'] == 'CLS-500'


def test_list_products_invalid_type(client):
    """Test /v2/products returns 400 for invalid productType."""
    response = client.get('/v2/products?productType=INVALID')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['code'] == 'INVALID_PARAMETER'


def test_composite_product_has_components(client):
    """Test that composite products have component structure."""
    response = client.get('/v2/product?mplvid=MPLV-99999')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data['productType'] == 'COMPOSITE'
    assert 'components' in data
    assert len(data['components']) > 0

    # Verify component structure
    component = data['components'][0]
    assert 'mplvid' in component
    assert 'quantity' in component
    assert 'relationship' in component
    assert 'redacted' in component


def test_product_with_barriers_structure(client):
    """Test that products with barriers have proper statusDetails."""
    response = client.get('/v2/product?mplvid=MPLV-54321')
    assert response.status_code == 200
    data = json.loads(response.data)

    status_details = data.get('statusDetails', {})
    barrier_reasons = status_details.get('barrierReasons', [])

    assert len(barrier_reasons) > 0
    barrier = barrier_reasons[0]
    assert 'code' in barrier
    assert 'message' in barrier
    assert 'fieldPath' in barrier
    assert 'severity' in barrier
    assert 'actionableSteps' in barrier
    assert 'remediationUrl' in barrier


def test_pipeline_status_structure(client):
    """Test that pipelineStatus has proper structure."""
    response = client.get('/v2/product?mplvid=MPLV-12345')
    assert response.status_code == 200
    data = json.loads(response.data)

    pipeline = data.get('pipelineStatus', {})
    assert 'overallStatus' in pipeline
    assert 'steps' in pipeline

    # Verify step structure
    steps = pipeline['steps']
    assert len(steps) > 0
    step = steps[0]
    assert 'code' in step
    assert 'name' in step
    assert 'status' in step
