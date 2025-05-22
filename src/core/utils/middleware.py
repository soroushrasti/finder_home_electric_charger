from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.utils.context_manager import CurrentRequestContext


class RequestHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        CurrentRequestContext.set_current_request(request)
        response = await call_next(request)
        return response
