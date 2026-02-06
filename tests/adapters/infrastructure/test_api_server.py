# -*- coding: utf-8 -*-
"""Tests for API Server"""

from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.adapters.infrastructure import create_api_server
from app.application.services import AssistantService
from app.domain.models import Response


class TestAPIServer:
    """Test cases for FastAPI server"""

    @pytest.fixture
    def mock_assistant_service(self):
        """Create a mocked AssistantService"""
        service = Mock(spec=AssistantService)
        service.wake_word = "xerife"
        service.is_running = False
        service._command_history = []
        return service

    @pytest.fixture
    def client(self, mock_assistant_service):
        """Create a test client with mocked service"""
        app = create_api_server(mock_assistant_service)
        return TestClient(app), mock_assistant_service

    def test_health_check(self, client):
        """Test health check endpoint"""
        test_client, _ = client
        response = test_client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_execute_command_success(self, client):
        """Test successful command execution"""
        test_client, service = client

        # Mock successful response
        service.process_command.return_value = Response(
            success=True,
            message="Command executed",
            data={"result": "ok"},
        )

        response = test_client.post(
            "/v1/execute",
            json={"command": "escreva hello"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Command executed"
        assert data["data"] == {"result": "ok"}
        service.process_command.assert_called_once_with("escreva hello")

    def test_execute_command_failure(self, client):
        """Test failed command execution"""
        test_client, service = client

        # Mock failed response
        service.process_command.return_value = Response(
            success=False,
            message="Invalid command",
            error="UNKNOWN_COMMAND",
        )

        response = test_client.post(
            "/v1/execute",
            json={"command": "invalid command"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Invalid command"
        assert data["error"] == "UNKNOWN_COMMAND"

    def test_execute_command_empty(self, client):
        """Test command execution with empty command"""
        test_client, _ = client

        response = test_client.post(
            "/v1/execute",
            json={"command": ""},
        )

        # Should fail validation (min_length=1)
        assert response.status_code == 422

    def test_execute_command_exception(self, client):
        """Test command execution with exception"""
        test_client, service = client

        # Mock exception
        service.process_command.side_effect = Exception("Test error")

        response = test_client.post(
            "/v1/execute",
            json={"command": "test"},
        )

        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]

    def test_get_status(self, client):
        """Test status endpoint"""
        test_client, service = client

        service.is_running = True

        response = test_client.get("/v1/status")

        assert response.status_code == 200
        data = response.json()
        assert data["app_name"] == "Jarvis Assistant"
        assert "version" in data
        assert data["is_active"] is True
        assert data["wake_word"] == "xerife"
        assert data["language"] == "pt-BR"

    def test_get_history_empty(self, client):
        """Test history endpoint with no commands"""
        test_client, service = client

        service.get_command_history.return_value = []

        response = test_client.get("/v1/history")

        assert response.status_code == 200
        data = response.json()
        assert data["commands"] == []
        assert data["total"] == 0

    def test_get_history_with_commands(self, client):
        """Test history endpoint with commands"""
        test_client, service = client

        service.get_command_history.return_value = [
            {
                "command": "escreva hello",
                "timestamp": "2024-01-01T00:00:00Z",
                "success": True,
                "message": "Typed: hello",
            },
            {
                "command": "aperte enter",
                "timestamp": "2024-01-01T00:00:01Z",
                "success": True,
                "message": "Pressed: enter",
            },
        ]

        response = test_client.get("/v1/history")

        assert response.status_code == 200
        data = response.json()
        assert len(data["commands"]) == 2
        assert data["total"] == 2
        assert data["commands"][0]["command"] == "escreva hello"
        assert data["commands"][1]["command"] == "aperte enter"

    def test_get_history_with_limit(self, client):
        """Test history endpoint with limit parameter"""
        test_client, service = client

        service.get_command_history.return_value = [
            {
                "command": "command1",
                "timestamp": "2024-01-01T00:00:00Z",
                "success": True,
                "message": "ok",
            },
        ]

        response = test_client.get("/v1/history?limit=10")

        assert response.status_code == 200
        service.get_command_history.assert_called_once_with(limit=10)

    def test_get_history_limit_validation(self, client):
        """Test history endpoint limit is capped"""
        test_client, service = client

        service.get_command_history.return_value = []

        # Should cap at 50
        response = test_client.get("/v1/history?limit=100")

        assert response.status_code == 200
        service.get_command_history.assert_called_once_with(limit=50)

    def test_api_documentation(self, client):
        """Test that API documentation is available"""
        test_client, _ = client

        response = test_client.get("/docs")
        assert response.status_code == 200

        response = test_client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()
