from fastapi import Request
from contextvars import ContextVar


class CurrentRequestContext:
    _current_request: ContextVar[Request] = ContextVar("current_request")

    @classmethod
    def set_current_request(cls, request: Request):
        cls._current_request.set(request)

    @classmethod
    def get_current_request(cls) -> Request:
        return cls._current_request.get()

    @classmethod
    def get_correlation_id(cls) -> str:
        try:
            request = cls.get_current_request()
            correlation_id = request.headers.get('Correlationid', 'UnknownCorrelationId')
        except LookupError:
            correlation_id = 'UnknownCorrelationId'
        return correlation_id
