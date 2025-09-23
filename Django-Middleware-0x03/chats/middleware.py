import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to this app is restricted during these hours."
            )
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    message_log = {}
    LIMIT = 5
    TIME_WINDOW = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()

            if ip not in self.message_log:
                self.message_log[ip] = []

            self.message_log[ip] = [
                ts for ts in self.message_log[ip] if now - ts < self.TIME_WINDOW
            ]

            if len(self.message_log[ip]) >= self.LIMIT:
                return HttpResponseForbidden(
                    "Message limit exceeded."
                )

            self.message_log[ip].append(now)

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            if not (user.is_superuser or user.is_staff):
                return HttpResponseForbidden("Access denied!!!")

        return self.get_response(request)