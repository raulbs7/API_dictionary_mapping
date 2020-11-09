#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Factories
'''

import urllib.parse
from restdict.client import RestDict
from restdict.server import DictServer


def new_server(server_address):
    '''
    Create new Web server with API REST
    '''
    return DictServer(server_address)


def new_client(server_api_uri, dict_id=None):
    '''
    Create new client connected to a given API URI
    '''
    return RestDict(server_api_uri, dict_id)