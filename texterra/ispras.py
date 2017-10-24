# -*- coding: utf-8 -*-
"""
Tools for accessing ISPRAS API
"""
import requests


class API(object):
    """ This class provides methods for sending GET and POST requests to ISPRAS API. """

    api_url = 'http://api.ispras.ru/{0}/{1}/'

    def __init__(self, key=None, name=None, ver=None, host=None):
        """
        If no host is specified, creates an API access object for the given ISPRAS service.

        :param key: API access key
        :param name: name of the ISPRAS service to be used
        :param ver: version of the ISPRAS service to be used
        :param host: a custom host for accessing ISPRAS services
        """
        if host is not None:
            self.url = host
            self.apikey = key
        else:
            if key is not None and len(key) == 40:
                self.apikey = key
                self.service_name = name
                self.service_ver = ver
                self.url = API.api_url.format(name, ver)
            else:
                raise ValueError('Invalid API key. Please provide a proper API key.')

    def get(self, path, params, headers=None):
        """ Method for invoking ISPRAS API GET request """
        return self._http_request(path, params, headers=headers)

    def post(self, path, params, data=None, json=None, headers=None):
        """ Method for invoking ISPRAS API POST request """
        return self._http_request(path, params, headers=headers, data=data, json=json)

    def _http_request(self, path, params, data=None, json=None, headers=None):

        headers = headers or {'Accept': 'application/json'}
        url = self._get_request_url(path)
        params = self._get_request_params(params)

        if data is None and json is None:
            page = requests.get(url, params=params, headers=headers, timeout=60)
        else:
            page = requests.post(url, params=params, headers=headers, data=data, json=json, timeout=60)

        return self._process_page(page)

    def _process_page(self, page):
        page.raise_for_status()  # raises exception if not successful
        return page.json()

    def _get_request_url(self, path):
        return '{0}{1}'.format(self.url, path)

    def _get_request_params(self, params):
        if self.apikey is not None:
            params['apikey'] = self.apikey
        return params
