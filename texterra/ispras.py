# -*- coding: utf-8 -*-
"""
Tools for accessing ISPRAS API
"""
import requests


class API(object):
    """ This class provides methods for sending GET and POST requests to ISPRAS API. """

    def __init__(self, key=None, host=None):
        if host is not None:
            self.url = host
        else:
            raise ValueError('Host is not specified.')

        if key is not None and len(key) == 40:
            self.apikey = key
        else:
            raise ValueError('Invalid API key. Please provide a proper API key.')

    def get(self, url, params, headers=None):
        """ Method for invoking ISPRAS API GET request """
        return self._http_request(url, params=params, headers=headers)

    def post(self, url, params, data=None, json=None, headers=None):
        """ Method for invoking ISPRAS API POST request """
        return self._http_request(url, params=params, headers=headers, data=data, json=json)

    def _http_request(self, url, params, data=None, json=None, headers=None):

        if 'apikey' not in params:
            raise ValueError('apikey not specified in params')

        headers = headers or {'Accept': 'application/json'}

        if data is None and json is None:
            page = requests.get(url, params=params, headers=headers, timeout=60)
        else:
            page = requests.post(url, params=params, headers=headers, data=data, json=json, timeout=60)

        return self._process_page(page)

    def _process_page(self, page):
        page.raise_for_status()  # raises exception if not successful
        return page.json()
