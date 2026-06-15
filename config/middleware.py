from django.utils import translation

from src.tournaments.developer_credit import credit_html, credit_is_present


class AdminUkrainianMiddleware:
    """Завжди українська в /admin/; без чеської/польської з браузера."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            translation.activate("uk")
            request.LANGUAGE_CODE = "uk"

        response = self.get_response(request)

        if request.path.startswith("/admin/"):
            response.headers.setdefault("Content-Language", "uk")

        return response


class DeveloperCreditMiddleware:
    """Гарантує наявність кредиту PrometeyLabs у публічних HTML-відповідях."""

    SKIP_PREFIXES = ("/admin/", "/static/", "/media/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self._ensure_credit(request, response)

    def _ensure_credit(self, request, response):
        if any(request.path.startswith(prefix) for prefix in self.SKIP_PREFIXES):
            return response

        content_type = response.get("Content-Type", "")
        if response.status_code != 200 or "text/html" not in content_type:
            return response

        charset = response.charset or "utf-8"
        try:
            html = response.content.decode(charset)
        except (UnicodeDecodeError, LookupError):
            return response

        if credit_is_present(html):
            return response

        snippet = credit_html()
        footer_close = html.lower().rfind("</footer>")
        if footer_close != -1:
            html = html[:footer_close] + snippet + html[footer_close:]
        else:
            body_close = html.lower().rfind("</body>")
            if body_close == -1:
                return response
            html = html[:body_close] + snippet + html[body_close:]

        response.content = html.encode(charset)
        if "Content-Length" in response:
            del response["Content-Length"]
        return response
