from requests import ConnectionError
import requests


class Connection(object):

    def __init__(self, auth):
        self.s = requests.Session()
        self.s.auth = auth

    def __del__(self):
        self.s.close()

    @staticmethod
    def validate_response(response):
        code = response.status_code
        if 200 > code or code > 299:
            raise ConnectionError("{code}: {text}".format(code=code, text=response.text))

    def get(self, url, params=None, **kwargs):
        response = self.s.get(url, params=params, **kwargs)
        self.validate_response(response)
        return response

    def post(self, url, data=None, json=None, **kwargs):
        response = self.s.post(url, data=data, json=json, **kwargs)
        self.validate_response(response)
        return response

    def delete(self, url, **kwargs):
        response = self.s.delete(url, **kwargs)
        self.validate_response(response)
        return response

    def patch(self, url, data, **kwargs):
        response = self.s.patch(url, data=data, **kwargs)
        self.validate_response(response)
        return response
