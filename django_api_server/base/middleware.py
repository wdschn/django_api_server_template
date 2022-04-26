import time
import uuid
from django.conf import settings


class ProcessDurationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)
        response['X-Page-Duration-ms'] = int((time.time() - start_time) * 1000)
        return response


class RequestIdMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        request_id_header_name = getattr(settings, 'REQUEST_ID_HEADER_NAME', None)
        if request_id_header_name:
            request_id = request.META.get(request_id_header_name, None)
            if request_id is None:
                request_id = uuid.uuid4().hex
            request.id = request_id
        response = self.get_response(request)

        if getattr(request, 'id', None):
            response[request_id_header_name] = request.id
        return response
