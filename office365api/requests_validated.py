import requests


def get(url, *args, **kwargs):
    response = requests.get(url, *args, **kwargs)
    if 200 > response.status_code or response.status_code > 299:
        raise requests.ConnectionError("{code}: {text}"
                                       .format(code=response.status_code, text=response.text))
    return response
