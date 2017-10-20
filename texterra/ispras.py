# -*- coding: utf-8 -*-
import requests


class API(object):
    """ Class for accessing ISPRAS API. """

    API_URL = 'http://api.ispras.ru/{0}/{1}/'

    def __init__(self, key=False, name=None, ver=None, host=None):
        if host is not None:
            self.apikey = key
            self.url = host
        else:
            if len(key) == 40:
                self.service_name = name
                self.service_version = ver
                self.apikey = key
                self.url = API.API_URL.format(name, ver)
            else:
                raise ValueError('Invalid API key. Please provide proper API key.')

    def get(self, path, request_params, fmt='json'):
        """Method for invoking ISPRAS API GET request"""
        url = self.url + path
        if self.apikey:
            request_params['apikey'] = self.apikey
        page = requests.get(url, params=request_params, headers=self._headers(fmt), timeout=60)
        if page.status_code == 200:
            return self._parse(page, fmt)
        else:
            page.raise_for_status()

    def post(self, path, params, data=None, fmt='json', json=None, headers=None):
        """ Method for invoking ISPRAS API POST request """
        if self.apikey:
            params['apikey'] = self.apikey

        if headers is None:
            headers = self._headers(fmt)

        page = requests.post(self.url + path, params=params, headers=headers, data=data, json=json, timeout=60)
        page.raise_for_status()  # raises exception if not successful

        return self._parse(page, fmt)

    def _parse(self, page, fmt='json'):
        if fmt == 'json':
            return page.json()
        else:
            return page.text

    def _headers(self, fmt='json'):
        headers = {'Accept': 'application/json'}
        return headers
