from django.conf import settings
from rest_framework.renderers import JSONRenderer


class CustomJsonRenderer(JSONRenderer):
    media_type = 'application/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # request = renderer_context.get('request')
        response = renderer_context.get('response')

        response_code = response.status_code
        response_data = data

        if isinstance(data, dict) and hasattr(data, 'code'):
            response_code = data.pop('code')

        if 200 <= response_code < 300:
            response_data = {'code': response_code, 'data': data}

        elif 400 <= response_code < 500:
            if response_code == 401:
                response_data = {'msg': "UNAUTHORIZED", 'code': "01"}
            elif isinstance(data, dict):
                if data.get("errors"):
                    response_data = {
                        'msg': '、'.join(data.get("errors")),
                        'code': data.get("code", response_code),
                    }
                else:
                    response_data = {
                        'msg': data,
                        'code': data.get("code", response_code)
                    }
            elif isinstance(data, list):
                response_data = {
                    'msg': ''.join(data),
                    'code': response_code
                }
            elif isinstance(data, str):
                response_data = {
                    'msg': data,
                    'code': response_code
                }
        elif response_code >= 500:
            response_data = {
                'code': response_code,
                'msg': 'Internal Server Error' if settings.DEBUG is False else data
            }

        return super(CustomJsonRenderer, self).render(response_data, accepted_media_type, renderer_context)
