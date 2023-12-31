class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META['Custom-Header'] = 'https://ecomm-store1.web.app'

        response = self.get_response(request)
        return response
