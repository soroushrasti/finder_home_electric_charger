from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.utils.context_manager import CurrentRequestContext


class RequestHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        CurrentRequestContext.set_current_request(request)
        response = await call_next(request)
        return response


from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        print("Request payload:", body.decode())
        print("Request header:", request.headers)

        response = await call_next(request)

        # Read and print response body
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        print("Response:", response_body.decode())

        # Return a new Response with the original body
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
