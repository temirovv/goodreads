class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        print(f'before {request.path=}')
        response = self.get_response(request)
        print(f"After {request.path=}")

        return response
