class AllowAddProductsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Temporarily bypass authentication for the add-all-products endpoint
        # WARNING: Remove this middleware in production!
        if request.method == 'POST' and request.path == '/api/products/add-all/':
            # Simulate an authenticated user or just bypass authentication checks downstream
            # For simplicity, we'll just let the request proceed without an authenticated user
            # This relies on the view itself having AllowAny permission
            request._authenticator = None # Bypass DRF's authentication
            request.user = None # Ensure no user is attached
            request._not_authenticated = True # Hint to DRF that authentication was skipped

        response = self.get_response(request)
        return response 