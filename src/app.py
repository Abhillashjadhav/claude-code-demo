"""
Task Echo API - A simple Flask REST API endpoint for echoing task data.

This module implements a REST API that accepts task information via POST
and echoes it back to confirm receipt.
"""

from flask import Flask, request, jsonify
from typing import Tuple, Dict, Any


app = Flask(__name__)

# Configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max payload size
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


@app.route('/task', methods=['POST'])
def echo_task() -> Tuple[Dict[str, Any], int]:
    """
    Echo task endpoint - accepts task data and returns it in a confirmation response.

    Expected request format:
        POST /task
        Content-Type: application/json
        Body: {"task": "some task description"}

    Success response format:
        Status: 200 OK
        Body: {"received": "some task description"}

    Returns:
        Tuple containing response dict and HTTP status code

    Raises:
        Returns appropriate error responses for invalid requests
    """
    # Check if the request has JSON content
    if not request.is_json:
        return jsonify({
            'error': 'Invalid request format',
            'message': 'Content-Type must be application/json'
        }), 400

    # Get the JSON data
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'error': 'Invalid JSON',
            'message': f'Failed to parse JSON: {str(e)}'
        }), 400

    # Check if data is None or not a dictionary
    if data is None or not isinstance(data, dict):
        return jsonify({
            'error': 'Invalid request body',
            'message': 'Request body must be a JSON object'
        }), 400

    # Check if 'task' field is present
    if 'task' not in data:
        return jsonify({
            'error': 'Missing required field',
            'message': 'Request must include a "task" field'
        }), 400

    # Get the task value
    task = data['task']

    # Validate task is a string
    if not isinstance(task, str):
        return jsonify({
            'error': 'Invalid task type',
            'message': 'Task must be a string'
        }), 400

    # Return the received task
    return jsonify({
        'received': task
    }), 200


@app.route('/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, str], int]:
    """
    Health check endpoint.

    Returns:
        Tuple containing health status and HTTP 200
    """
    return jsonify({'status': 'healthy'}), 200


@app.errorhandler(413)
def request_entity_too_large(error) -> Tuple[Dict[str, Any], int]:
    """
    Handle requests that exceed the maximum content length.

    Args:
        error: The error that triggered this handler

    Returns:
        Tuple containing error response and HTTP 413 status
    """
    return jsonify({
        'error': 'Payload too large',
        'message': f'Request payload exceeds maximum size of {MAX_CONTENT_LENGTH} bytes'
    }), 413


if __name__ == '__main__':
    # Run the development server
    app.run(debug=True, host='0.0.0.0', port=5000)
