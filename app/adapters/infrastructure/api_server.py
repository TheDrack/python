# -*- coding: utf-8 -*-
"""FastAPI Server for Headless Control Interface"""

import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.adapters.infrastructure.api_models import (
    CommandHistoryItem,
    ExecuteRequest,
    ExecuteResponse,
    HistoryResponse,
    StatusResponse,
)
from app.application.services import AssistantService
from app.core.config import settings

logger = logging.getLogger(__name__)


def create_api_server(assistant_service: AssistantService) -> FastAPI:
    """
    Create and configure the FastAPI application

    Args:
        assistant_service: Injected AssistantService instance

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title=settings.app_name + " API",
        version=settings.version,
        description="Headless control interface for the AI assistant",
    )

    @app.post("/v1/execute", response_model=ExecuteResponse)
    async def execute_command(request: ExecuteRequest) -> ExecuteResponse:
        """
        Execute a command and return the result

        Args:
            request: Command execution request

        Returns:
            Command execution response
        """
        try:
            logger.info(f"Executing command via API: {request.command}")
            response = assistant_service.process_command(request.command)

            return ExecuteResponse(
                success=response.success,
                message=response.message,
                data=response.data,
                error=response.error,
            )
        except Exception as e:
            logger.error(f"Error executing command: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    @app.get("/v1/status", response_model=StatusResponse)
    async def get_status() -> StatusResponse:
        """
        Get the current system status

        Returns:
            System status information
        """
        try:
            return StatusResponse(
                app_name=settings.app_name,
                version=settings.version,
                is_active=assistant_service.is_running,
                wake_word=assistant_service.wake_word,
                language=settings.language,
            )
        except Exception as e:
            logger.error(f"Error getting status: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    @app.get("/v1/history", response_model=HistoryResponse)
    async def get_history(limit: int = 5) -> HistoryResponse:
        """
        Get recent command history

        Args:
            limit: Maximum number of commands to return (default: 5, max: 50)

        Returns:
            Command history response
        """
        try:
            # Limit to reasonable range
            limit = max(1, min(limit, 50))
            history = assistant_service.get_command_history(limit=limit)

            return HistoryResponse(
                commands=[
                    CommandHistoryItem(
                        command=item["command"],
                        timestamp=item["timestamp"],
                        success=item["success"],
                        message=item["message"],
                    )
                    for item in history
                ],
                total=len(history),
            )
        except Exception as e:
            logger.error(f"Error getting history: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    @app.get("/health")
    async def health_check():
        """
        Health check endpoint

        Returns:
            Simple health check response
        """
        return JSONResponse(content={"status": "healthy"})

    return app
