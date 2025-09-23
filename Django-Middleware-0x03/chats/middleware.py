# messaging_app/middleware.py
import logging
import os
from datetime import datetime
from django.conf import settings

# Set absolute path for requests.log
LOG_FILE = os.path.join(settings.BASE_DIR, "requests.log")

# Configure logger
logger = logging.getLogger("request_logger")
file_handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Middleware to log all incoming requests with timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Identify user
        user = (
            request.user.username
            if hasattr(request, "user") and request.user.is_authenticated
            else "Anonymous"
        )

        # Log the request
        logger.info(f"User: {user} - Method: {request.method} - Path: {request.get_full_path()}")

        # Continue processing the request
        response = self.get_response(request)
        return response
