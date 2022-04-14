import time


class ProcessDurationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        response['X-Page-Duration-ms'] = int((time.time() - start_time) * 1000)
        return response

