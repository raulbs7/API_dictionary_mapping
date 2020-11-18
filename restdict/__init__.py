#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Factories
'''

import urllib.parse
import uuid

import requests

from restdict.client import RestDict
from restdict.server import DictServer


def new_server(server_address):
    '''
    Create new Web server with API REST
    '''
    return DictServer(server_address)


def new_client(server_api_uri, dict_name=None):
    '''
    Create new client connected to a given API URI
    '''
    return RestDict(server_api_uri, dict_name)


def connect_restdict(server_api_uri, dict_name):
    result = requests.get(f'{server_api_uri}/{dict_name}')
    if result.status_code == 404:
        raise Exception
    return RestDict(server_api_uri, dict_name)


def delete_restdict(server_api_uri, dict_name):
    result = requests.delete(f'{server_api_uri}/{dict_name}')
    if result.status_code == 404:
        raise Exception