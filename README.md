# Task Echo API

A simple, reliable REST API for echoing task data. Built with Flask, this API provides a foundation for integration testing and validates that task information can be submitted and received correctly.

## Overview

The Task Echo API accepts task information via a POST endpoint and immediately echoes it back in a confirmation response. This creates a closed feedback loop that validates both submission and retrieval are working correctly, making it ideal for:

- Integration testing for external systems
- Validating API communication patterns
- Self-verifying system integrations
- Demonstrating REST API best practices

## Features

- Simple REST API with JSON request/response format
- Comprehensive input validation and error handling
- Support for unicode and special characters
- Large payload handling (up to 16MB)
- Health check endpoint for monitoring
- Detailed error messages for debugging

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd claude-code-demo
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the API

### Development Server

Start the Flask development server:

```bash
python src/app.py
```

The API will be available at `http://localhost:5000`

### Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app
```

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Echo Task
Submit task data and receive a confirmation echo.

**Endpoint**: `POST /task`

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "task": "Your task description here"
}
```

**Success Response**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "received": "Your task description here"
}
```

**Error Responses**:

| Status Code | Error | Description |
|-------------|-------|-------------|
| 400 | Invalid request format | Content-Type must be application/json |
| 400 | Invalid JSON | Request body contains malformed JSON |
| 400 | Missing required field | Request must include a "task" field |
| 400 | Invalid task type | Task must be a string |
| 413 | Payload too large | Request exceeds 16MB limit |

#### 2. Health Check
Verify the API is running and healthy.

**Endpoint**: `GET /health`

**Success Response**:
- **Status Code**: 200 OK
- **Response Body**:
```json
{
  "status": "healthy"
}
```

## Usage Examples

### Using cURL

**Submit a simple task**:
```bash
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{"task": "Complete project documentation"}'
```

**Response**:
```json
{
  "received": "Complete project documentation"
}
```

**Check health status**:
```bash
curl http://localhost:5000/health
```

### Using Python requests

```python
import requests

# Submit a task
response = requests.post(
    'http://localhost:5000/task',
    json={'task': 'Deploy to production'}
)

if response.status_code == 200:
    data = response.json()
    print(f"Task received: {data['received']}")
else:
    print(f"Error: {response.json()}")

# Health check
health_response = requests.get('http://localhost:5000/health')
print(f"API Status: {health_response.json()['status']}")
```

### Using JavaScript fetch

```javascript
// Submit a task
fetch('http://localhost:5000/task', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    task: 'Update user documentation'
  })
})
  .then(response => response.json())
  .then(data => console.log('Task received:', data.received))
  .catch(error => console.error('Error:', error));

// Health check
fetch('http://localhost:5000/health')
  .then(response => response.json())
  .then(data => console.log('API Status:', data.status));
```

## Special Characters and Unicode Support

The API fully supports special characters, unicode, and multi-line strings:

```bash
# Task with unicode
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{"task": "Hello 世界 🌍 café"}'

# Task with newlines
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{"task": "Line 1\nLine 2\nLine 3"}'

# Task with special characters
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{"task": "Task with \"quotes\" and \u0027apostrophes\u0027"}'
```

## Error Handling Examples

**Missing task field**:
```bash
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{"other_field": "value"}'
```
Response (400):
```json
{
  "error": "Missing required field",
  "message": "Request must include a \"task\" field"
}
```

**Invalid task type**:
```bash
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{"task": 123}'
```
Response (400):
```json
{
  "error": "Invalid task type",
  "message": "Task must be a string"
}
```

**Invalid content type**:
```bash
curl -X POST http://localhost:5000/task \
  -H "Content-Type: text/plain" \
  -d "task=something"
```
Response (400):
```json
{
  "error": "Invalid request format",
  "message": "Content-Type must be application/json"
}
```

## Running Tests

The project includes a comprehensive test suite with 28 tests covering happy paths, edge cases, error handling, and boundary conditions.

### Run all tests:
```bash
pytest
```

### Run tests with verbose output:
```bash
pytest -v
```

### Run tests with coverage report:
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

The test coverage is currently at 93%, with reports available in `htmlcov/index.html`.

### Run specific test classes:
```bash
# Test happy path scenarios
pytest tests/test_app.py::TestTaskEchoHappyPath -v

# Test error handling
pytest tests/test_app.py::TestTaskEchoInvalidRequests -v

# Test special characters
pytest tests/test_app.py::TestTaskEchoSpecialCharacters -v
```

## Project Structure

```
claude-code-demo/
├── src/
│   └── app.py              # Main Flask application
├── tests/
│   └── test_app.py         # Comprehensive test suite
├── docs/
│   └── requirements.md     # Product requirements document
├── README.md               # This file
├── CHANGELOG.md            # Project changelog
└── requirements.txt        # Python dependencies
```

## Configuration

The API includes the following configurable settings in `src/app.py`:

- **MAX_CONTENT_LENGTH**: 16MB (16 * 1024 * 1024 bytes)
  - Maximum size for request payloads
  - Prevents memory exhaustion from large requests

- **Development Server**:
  - Host: `0.0.0.0` (accessible from all network interfaces)
  - Port: `5000`
  - Debug: `True` (disable in production)

## Validation Rules

The `/task` endpoint enforces the following validation rules:

1. **Content-Type**: Must be `application/json`
2. **Request Body**: Must be a valid JSON object (not array or primitive)
3. **task field**: Required, must be present in the JSON object
4. **task value**: Must be a string type (not number, boolean, null, array, or object)
5. **Payload Size**: Must not exceed 16MB

Empty strings are allowed and will be echoed back as-is.

## Development

This project was built using a multi-agent development workflow:

1. **Planner Agent**: Created the product requirements document
2. **Implementer Agent**: Built the Flask API implementation
3. **Tester Agent**: Wrote and executed comprehensive tests
4. **Documentation Writer Agent**: Created this documentation

## Contributing

When contributing to this project:

1. Update `docs/requirements.md` if adding new features
2. Add comprehensive tests to maintain 90%+ coverage
3. Update this README with new usage examples
4. Update CHANGELOG.md with your changes

## License

This project is part of the Claude Multi-Agent Demo.

## Support

For issues, questions, or feature requests, please refer to the project repository.

---

**Last Updated**: 2025-11-10
**Version**: 1.0.0
**Test Coverage**: 93%
**Test Status**: 28 passing tests
