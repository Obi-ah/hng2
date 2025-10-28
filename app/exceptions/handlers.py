import json

from fastapi.exceptions import RequestValidationError

from app.exceptions.app_exceptions import NotFoundError, DatabaseError
from fastapi import Request, Response, status


def register_exception_handlers(app):
    """Attach all custom exception handlers to FastAPI app."""


    @app.exception_handler(NotFoundError)
    def not_found_handler(request: Request, exc: NotFoundError):
        return Response(
            content=json.dumps({"error": str(exc)}),
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json"
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        first_error = errors[0] if errors else {}
        message = first_error.get("msg", "Invalid input")

        return Response(
            content=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="application/json"
        )


    @app.exception_handler(DatabaseError)
    def database_handler(request: Request, exc: DatabaseError):
        return Response(
            content=json.dumps({"error": str(exc)}),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )

    @app.exception_handler(Exception)
    def generic_handler(request: Request, exc: Exception):
        # Generic fallback for unexpected errors
        return Response(
            content=json.dumps({"error": "Internal server error", "detail": str(exc)}),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )