"""
Comprehensive test suite for the Task Echo API.

Tests cover happy path scenarios, edge cases, error handling, and boundary conditions.
"""

import pytest
import json
from src.app import app


@pytest.fixture
def client():
    """
    Create a test client for the Flask application.

    Yields:
        FlaskClient: Test client for making requests
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestTaskEchoHappyPath:
    """Tests for successful task echo scenarios."""

    def test_echo_simple_task(self, client):
        """Test echoing a simple task string."""
        response = client.post(
            '/task',
            data=json.dumps({'task': 'Complete project documentation'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'received' in data
        assert data['received'] == 'Complete project documentation'

    def test_echo_task_with_spaces(self, client):
        """Test echoing a task with multiple spaces."""
        response = client.post(
            '/task',
            data=json.dumps({'task': '   Task with   multiple   spaces   '}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == '   Task with   multiple   spaces   '

    def test_echo_numeric_string_task(self, client):
        """Test echoing a task that contains only numbers but is a string."""
        response = client.post(
            '/task',
            data=json.dumps({'task': '123456'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == '123456'


class TestTaskEchoEmptyAndMissingData:
    """Tests for empty and missing data scenarios."""

    def test_empty_task_string(self, client):
        """Test echoing an empty task string."""
        response = client.post(
            '/task',
            data=json.dumps({'task': ''}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'received' in data
        assert data['received'] == ''

    def test_missing_task_field(self, client):
        """Test request without the required task field."""
        response = client.post(
            '/task',
            data=json.dumps({'other_field': 'value'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'message' in data
        assert 'task' in data['message'].lower()

    def test_empty_json_object(self, client):
        """Test request with empty JSON object."""
        response = client.post(
            '/task',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestTaskEchoSpecialCharacters:
    """Tests for special characters and unicode handling."""

    def test_task_with_quotes(self, client):
        """Test task containing various quote characters."""
        response = client.post(
            '/task',
            data=json.dumps({'task': 'Task with "double" and \'single\' quotes'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == 'Task with "double" and \'single\' quotes'

    def test_task_with_newlines(self, client):
        """Test task containing newline characters."""
        response = client.post(
            '/task',
            data=json.dumps({'task': 'Line 1\nLine 2\nLine 3'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == 'Line 1\nLine 2\nLine 3'

    def test_task_with_unicode(self, client):
        """Test task containing unicode characters."""
        response = client.post(
            '/task',
            data=json.dumps({'task': 'Hello 世界 🌍 café'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == 'Hello 世界 🌍 café'

    def test_task_with_special_symbols(self, client):
        """Test task containing special symbols."""
        response = client.post(
            '/task',
            data=json.dumps({'task': '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'

    def test_task_with_backslashes(self, client):
        """Test task containing backslashes."""
        response = client.post(
            '/task',
            data=json.dumps({'task': 'Path\\to\\file'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == 'Path\\to\\file'


class TestTaskEchoLargePayloads:
    """Tests for large payload handling."""

    def test_large_task_within_limit(self, client):
        """Test task with large but acceptable size."""
        large_task = 'x' * 10000  # 10KB task
        response = client.post(
            '/task',
            data=json.dumps({'task': large_task}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == large_task

    def test_very_large_task_within_limit(self, client):
        """Test task approaching the size limit."""
        # Create a task that's about 1MB (well within 16MB limit)
        large_task = 'x' * (1024 * 1024)
        response = client.post(
            '/task',
            data=json.dumps({'task': large_task}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['received']) == len(large_task)


class TestTaskEchoInvalidRequests:
    """Tests for invalid request handling."""

    def test_invalid_json_format(self, client):
        """Test request with malformed JSON."""
        response = client.post(
            '/task',
            data='{"task": invalid json}',
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_non_json_content_type(self, client):
        """Test request without JSON content type."""
        response = client.post(
            '/task',
            data='task=something',
            content_type='application/x-www-form-urlencoded'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'json' in data['message'].lower()

    def test_task_as_integer(self, client):
        """Test request where task value is an integer instead of string."""
        response = client.post(
            '/task',
            data=json.dumps({'task': 123}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'string' in data['message'].lower()

    def test_task_as_array(self, client):
        """Test request where task value is an array instead of string."""
        response = client.post(
            '/task',
            data=json.dumps({'task': ['item1', 'item2']}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_task_as_object(self, client):
        """Test request where task value is an object instead of string."""
        response = client.post(
            '/task',
            data=json.dumps({'task': {'subtask': 'value'}}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_task_as_null(self, client):
        """Test request where task value is null."""
        response = client.post(
            '/task',
            data=json.dumps({'task': None}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_json_array_instead_of_object(self, client):
        """Test request where body is a JSON array instead of object."""
        response = client.post(
            '/task',
            data=json.dumps(['task1', 'task2']),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestTaskEchoConcurrency:
    """Tests for concurrent request handling."""

    def test_rapid_sequential_requests(self, client):
        """Test multiple rapid sequential task submissions."""
        tasks = [f'Task {i}' for i in range(10)]
        responses = []

        for task in tasks:
            response = client.post(
                '/task',
                data=json.dumps({'task': task}),
                content_type='application/json'
            )
            responses.append(response)

        # Verify all requests succeeded
        assert all(r.status_code == 200 for r in responses)

        # Verify each task was echoed correctly
        for i, response in enumerate(responses):
            data = response.get_json()
            assert data['received'] == f'Task {i}'


class TestTaskEchoBoundaryConditions:
    """Tests for boundary conditions."""

    def test_minimum_valid_task(self, client):
        """Test with minimum valid task (single character)."""
        response = client.post(
            '/task',
            data=json.dumps({'task': 'x'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == 'x'

    def test_task_with_only_whitespace(self, client):
        """Test task containing only whitespace."""
        response = client.post(
            '/task',
            data=json.dumps({'task': '   '}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == '   '

    def test_task_with_tabs_and_newlines(self, client):
        """Test task with tabs and newlines."""
        response = client.post(
            '/task',
            data=json.dumps({'task': '\t\n\r\n'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['received'] == '\t\n\r\n'


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'healthy'


class TestMethodNotAllowed:
    """Tests for incorrect HTTP methods."""

    def test_get_method_not_allowed(self, client):
        """Test that GET method is not allowed on /task endpoint."""
        response = client.get('/task')
        assert response.status_code == 405

    def test_put_method_not_allowed(self, client):
        """Test that PUT method is not allowed on /task endpoint."""
        response = client.put(
            '/task',
            data=json.dumps({'task': 'test'}),
            content_type='application/json'
        )
        assert response.status_code == 405

    def test_delete_method_not_allowed(self, client):
        """Test that DELETE method is not allowed on /task endpoint."""
        response = client.delete('/task')
        assert response.status_code == 405
