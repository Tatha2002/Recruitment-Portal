import time

from django.shortcuts import redirect


class RequestLogMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        # Block unauthenticated dashboard access
        if request.path.startswith('/dashboard/'):

            if not request.user.is_authenticated:

                return redirect('login')

        response = self.get_response(request)

        processing_time = (
            time.time() - start_time
        )

        if request.user.is_authenticated:
            role = request.user.role
        else:
            role = 'Anonymous'

        print(
            f"PATH={request.path} | "
            f"METHOD={request.method} | "
            f"TIME={processing_time:.4f}s | "
            f"ROLE={role}"
        )

        return response