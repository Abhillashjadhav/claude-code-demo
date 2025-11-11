"""Read API 2.0 MVP Demo - Flask application."""
from flask import Flask, request, jsonify, render_template
from src.data import get_store

app = Flask(__name__, template_folder='../templates')


def parse_bool(value):
    """Parse boolean query parameter."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    return value.lower() in ('true', '1', 'yes')


@app.route('/', methods=['GET'])
def index():
    """Serve the interactive dashboard UI."""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


@app.route('/v2/product', methods=['GET'])
def get_product():
    """
    Get a single product by MPLVID.

    Query params:
        mplvid (required): MarketplaceListingVariantID
        market (optional): Market context (e.g., US, CA)

    Returns:
        200: Product object
        400: Missing or invalid parameters
        404: Product not found
    """
    mplvid = request.args.get('mplvid')
    market = request.args.get('market')

    if not mplvid:
        return jsonify({
            "error": "Missing required parameter 'mplvid'",
            "code": "MISSING_PARAMETER"
        }), 400

    store = get_store()
    product = store.get_product(mplvid, market)

    if product is None:
        return jsonify({
            "error": f"Product not found: {mplvid}",
            "code": "NOT_FOUND"
        }), 404

    return jsonify(product), 200


@app.route('/v2/group', methods=['GET'])
def get_group():
    """
    Get a variant group by variantGroupId.

    Query params:
        variantGroupId (required): Variant group identifier
        market (optional): Market context (e.g., US, CA)

    Returns:
        200: Variant group object
        400: Missing or invalid parameters
        404: Group not found
    """
    variant_group_id = request.args.get('variantGroupId')
    market = request.args.get('market')

    if not variant_group_id:
        return jsonify({
            "error": "Missing required parameter 'variantGroupId'",
            "code": "MISSING_PARAMETER"
        }), 400

    store = get_store()
    group = store.get_group(variant_group_id, market)

    if group is None:
        return jsonify({
            "error": f"Variant group not found: {variant_group_id}",
            "code": "NOT_FOUND"
        }), 404

    return jsonify(group), 200


@app.route('/v2/products', methods=['GET'])
def list_products():
    """
    List products with optional filters.

    Query params (all optional):
        market: Filter by market context
        classId: Filter by class ID
        productType: Filter by product type (SIMPLE, COMPOSITE, KIT)
        hasBarriers: Filter by presence of barriers (true/false)
        lastUpdatedAfter: Filter by lastUpdated timestamp (ISO 8601)

    Returns:
        200: List of products
        400: Invalid parameters
    """
    market = request.args.get('market')
    class_id = request.args.get('classId')
    product_type = request.args.get('productType')
    has_barriers_str = request.args.get('hasBarriers')
    last_updated_after = request.args.get('lastUpdatedAfter')

    # Parse boolean parameter
    has_barriers = parse_bool(has_barriers_str)

    # Validate productType if provided
    if product_type and product_type not in ['SIMPLE', 'COMPOSITE', 'KIT']:
        return jsonify({
            "error": f"Invalid productType: {product_type}. Must be SIMPLE, COMPOSITE, or KIT",
            "code": "INVALID_PARAMETER"
        }), 400

    try:
        store = get_store()
        products = store.list_products(
            market=market,
            class_id=class_id,
            product_type=product_type,
            has_barriers=has_barriers,
            last_updated_after=last_updated_after
        )

        return jsonify({
            "products": products,
            "count": len(products)
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Invalid query parameters: {str(e)}",
            "code": "INVALID_PARAMETER"
        }), 400


@app.route('/v2/product/<mplvid>/status', methods=['PUT'])
def update_product_status(mplvid):
    """
    Update product status (for demo purposes).

    Body params:
        status (required): New status (LIVE, BLOCKED, PROCESSING)

    Returns:
        200: Success message
        400: Invalid parameters
        404: Product not found
    """
    data = request.json or {}
    new_status = data.get('status')

    if not new_status:
        return jsonify({
            "error": "Missing required parameter 'status'",
            "code": "MISSING_PARAMETER"
        }), 400

    if new_status not in ['LIVE', 'BLOCKED', 'PROCESSING']:
        return jsonify({
            "error": f"Invalid status: {new_status}. Must be LIVE, BLOCKED, or PROCESSING",
            "code": "INVALID_PARAMETER"
        }), 400

    store = get_store()
    success = store.update_product_status(mplvid, new_status)

    if not success:
        return jsonify({
            "error": f"Product not found: {mplvid}",
            "code": "NOT_FOUND"
        }), 404

    return jsonify({
        "message": f"Product {mplvid} status updated to {new_status}",
        "mplvid": mplvid,
        "status": new_status
    }), 200


@app.route('/v2/product/<mplvid>/barriers', methods=['POST'])
def add_barrier(mplvid):
    """
    Add a barrier to a product (for demo purposes).

    Body params:
        code (required): Barrier code
        message (required): Error message
        fieldPath (optional): Field causing the barrier
        severity (optional): ERROR or WARNING

    Returns:
        200: Success message
        400: Invalid parameters
        404: Product not found
    """
    data = request.json or {}

    code = data.get('code')
    message = data.get('message')

    if not code or not message:
        return jsonify({
            "error": "Missing required parameters 'code' and 'message'",
            "code": "MISSING_PARAMETER"
        }), 400

    barrier = {
        "code": code,
        "message": message,
        "fieldPath": data.get('fieldPath', ''),
        "severity": data.get('severity', 'ERROR'),
        "actionableSteps": data.get('actionableSteps', []),
        "remediationUrl": data.get('remediationUrl', ''),
        "addedBy": "Demo User"
    }

    store = get_store()
    success = store.add_barrier(mplvid, barrier)

    if not success:
        return jsonify({
            "error": f"Product not found: {mplvid}",
            "code": "NOT_FOUND"
        }), 404

    return jsonify({
        "message": f"Barrier added to product {mplvid}",
        "mplvid": mplvid,
        "barrier": barrier
    }), 200


@app.route('/v2/product/<mplvid>/barriers', methods=['DELETE'])
def remove_barriers(mplvid):
    """
    Remove all barriers from a product (for demo purposes).

    Returns:
        200: Success message
        404: Product not found
    """
    store = get_store()
    success = store.remove_all_barriers(mplvid)

    if not success:
        return jsonify({
            "error": f"Product not found: {mplvid}",
            "code": "NOT_FOUND"
        }), 404

    return jsonify({
        "message": f"All barriers removed from product {mplvid}",
        "mplvid": mplvid
    }), 200


@app.route('/v2/reset', methods=['POST'])
def reset_data():
    """
    Reset all data to original state (for demo purposes).

    Returns:
        200: Success message
    """
    store = get_store()
    store.reset_data()

    return jsonify({
        "message": "Data reset to original state",
        "products": len(store.products),
        "groups": len(store.groups)
    }), 200


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        "error": "Endpoint not found",
        "code": "NOT_FOUND"
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return jsonify({
        "error": "Internal server error",
        "code": "INTERNAL_ERROR"
    }), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
