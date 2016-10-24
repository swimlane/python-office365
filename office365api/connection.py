from typing import Tuple
from requests import ConnectionError
import requests


class Connection(object):

    def __init__(self, auth: Tuple[str, str]):
        self.auth = auth

    @staticmethod
    def validate_response(response):
        code = response.status_code
        if 200 > code or code > 299:
            raise ConnectionError("{code}: {text}".format(code=code, text=response.text))

    def get(self, url, params=None, **kwargs):
        response = requests.get(url, params, **kwargs, auth=self.auth)
        self.validate_response(response)
        return response

    def post(self, url, data=None, json=None, **kwargs):
        response = requests.post(url, data, json, **kwargs, auth=self.auth)
        self.validate_response(response)
        return response

    def delete(self, url, **kwargs):
        response = requests.delete(url, **kwargs, auth=self.auth)
        self.validate_response(response)
        return response
