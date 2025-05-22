import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.config.logging_config import setup_logging

# Set up logging configuration
setup_logging()
logger = logging.getLogger(__name__)


class LogErrorsMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        # Check if response indicates an unhandled error (status code 500)
        if response.status_code >= 500:
            correlation_id = request.headers.get('Correlationid', 'unknown')
            logger.error(f" CorrelationID: {correlation_id} - Unhandled server error - {request.method} {request.url}")
            error_response_content = {
                "error": "Internal Server Error",
                "message": "An unexpected error occurred.",
                "correlation_id": correlation_id
            }
            return JSONResponse(content=error_response_content, status_code=response.status_code )
        return response

