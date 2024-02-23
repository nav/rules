class AuthenticationSimulationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.person = {
            "organization": {"name": "Acme"},
            "age": 24,
            "sex_at_birth": "male",
            "address_state": "CA",
            "address_country": "US",
        }
        response = self.get_response(request)
        return response
