from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import BlacklistedToken


class TokenBlacklistMiddleware(MiddlewareMixin):
    """
    Middleware to reject blacklisted tokens before processing any request.
    """

    def process_request(self, request):
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            if BlacklistedToken.objects.filter(token=token).exists():
                return JsonResponse({"error": "Token has been blacklisted"}, status=401)
