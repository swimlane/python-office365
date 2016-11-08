from requests import ConnectionError
import requests


class Connection(object):

    def __init__(self, auth):
        self.auth = auth

    @staticmethod
    def validate_response(response):
        code = response.status_code
        if 200 > code or code > 299:
            raise ConnectionError("{code}: {text}".format(code=code, text=response.text))

    def get(self, url, params=None, **kwargs):
        response = requests.get(url, params, auth=self.auth, **kwargs)
        self.validate_response(response)
        return response

    def post(self, url, data=None, json=None, **kwargs):
        response = requests.post(url, data, json, auth=self.auth, **kwargs)
        self.validate_response(response)
        return response

    def delete(self, url, **kwargs):
        response = requests.delete(url, auth=self.auth, **kwargs)
        self.validate_response(response)
        return response

    def patch(self, url, data, **kwargs):
        response = requests.patch(url=url, data=data, **kwargs)
        self.validate_response(response)
        return response
