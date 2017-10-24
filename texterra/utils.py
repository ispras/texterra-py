# -*- coding: utf-8 -*-
"""
Tools for HTTP JSON API
"""
import requests


class HttpBase(object):
    """ This class provides methods for sending GET and POST requests to JSON API. """

    def __init__(self, key, url):
        """
        :param url: base url for access
        """
        self.base_url = url
        self.apikey = key

    def get(self, path, params):
        """ Method for invoking API GET request """
        return self.custom_query(path, params)

    def post(self, path, params, json):
        """ Method for invoking API POST request """
        return self.custom_query(path, params, json)

    def custom_query(self, path, params, json=None):
        headers = {'Accept': 'application/json'}
        url = self.base_url + path
        if self.apikey:
            params['apikey'] = self.apikey

        if json is None:
            page = requests.get(url, params=params, headers=headers, timeout=60)
        else:
            page = requests.post(url, params=params, headers=headers, json=json, timeout=60)

        return self._process_page(page)

    def _process_page(self, page):
        page.raise_for_status()  # raises exception if not successful
        return page.json()
