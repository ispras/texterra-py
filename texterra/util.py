# -*- coding: utf-8 -*-
"""
Utility functions for online API.
"""
import requests


def get(url, params, headers=None):
    """ Method for invoking ISPRAS API GET request"""
    return _http_request(url, params=params, headers=headers)


def post(url, params, data=None, json=None, headers=None):
    """ Method for invoking ISPRAS API POST request """
    return _http_request(url, params=params, headers=headers, data=data, json=json)


def _http_request(url, params, data=None, json=None, headers=None):
    if 'apikey' not in params:
        raise ValueError('apikey not specified in params')

    headers = headers or {'Accept': 'application/json'}

    if data is None and json is None:
        page = requests.get(url, params=params, headers=headers, timeout=60)
    else:
        page = requests.post(url, params=params, headers=headers, data=data, json=json, timeout=60)

    return _process_page(page)


def _process_page(page):
    page.raise_for_status()  # raises exception if not successful
    return page.json()

