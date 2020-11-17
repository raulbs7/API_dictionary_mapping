#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pickle
import binascii
import uuid
from collections.abc import MutableMapping

import requests


def _marshall_(value):
    return binascii.b2a_base64(pickle.dumps(value))


def _unmarshall_(value):
    return pickle.loads(binascii.a2b_base64(value))


class RestDict(MutableMapping):
    def __init__(self, base_api_uri, id=None):
        self._uri_ = base_api_uri
        if not isinstance(id, str) and id is not None:
            raise TypeError(id)
        self._id_ = id
        if self._uri_.endswith('/'):
            self._uri_ = self._uri_[:-1]
        if self._id_ is None:
            while True:
                self._id_ = str(uuid.uuid4())
                result = requests.get(f'{self._uri_}/{self._id_}')
                if result.status_code not in [200, 201]:
                    break
        result = requests.put(f'{self._uri_}/{self._id_}')
        if result.status_code not in [200, 201]:
            raise ValueError(f'Cannot init dictionary: {result.status_code}')

    def keys(self):
        result = requests.get(f'{self._uri_}/{self._id_}/keys')
        if result.status_code != 200:
            raise ValueError(f'Cannot get keys, status code: {result.status_code}')
        try:
            result = json.loads(result.content.decode()).get('result', [])
        except Exception as error:
            raise ValueError(f'Cannot get keys: {error}')
        return result

    def values(self):
        result = requests.get(f'{self._uri_}/{self._id_}/values')
        if result.status_code != 200:
            raise ValueError(f'Cannot get keys, status code: {result.status_code}')
        try:
            result = json.loads(result.content.decode()).get('result', [])
        except Exception as error:
            raise ValueError(f'Cannot get keys: {error}')
        result_unmarshall = []
        for x in range(0, len(result)):
            result_unmarshall.append(_unmarshall_(result[x]))
        return result_unmarshall

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError(key)
        result = requests.get(f'{self._uri_}/{self._id_}/keys/{key}')
        if result.status_code == 404:
            raise KeyError(key)
        try:
            result = json.loads(result.content.decode())['result']
        except Exception as error:
            raise ValueError(f'Cannot get item: {error}')
        try:
            return _unmarshall_(result)
        except Exception as error:
            raise ValueError(f'Unmarshalling error: {error}')

    def __str__(self):
        result = requests.get(f'{self._uri_}/{self._id_}')
        if result.status_code != 200:
            raise ValueError(f'Cannot get str, status code: {result.status_code}')
        try:
            result = json.loads(result.content.decode()).get('result', [])
        except Exception as error:
            raise ValueError(f'Cannot get str: {error}')
        result_unmarshall = {}
        for key in result:
            result_unmarshall[key] = _unmarshall_(result[key])
        return str(result_unmarshall)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(key)
        if key in self.keys():
            result = requests.post(f'{self._uri_}/{self._id_}/keys/{key}', data=_marshall_(value))
        else:
            result = requests.put(f'{self._uri_}/{self._id_}/keys/{key}', data=_marshall_(value))
        if result.status_code not in [200, 201]:
            raise ValueError(f'Cannot set item: {result.status_code}')

    def __delitem__(self, key):
        if not isinstance(key, str):
            raise TypeError(key)
        result = requests.delete(f'{self._uri_}/{self._id_}/keys/{key}')

        if result.status_code == 404:
            raise KeyError(key)

    def __del__(self):
        result = requests.delete(f'{self._uri_}/{self._id_}')
        if result.status_code == 404:
            raise ValueError(f'Cannot delete dict: {result.status_code}')

    def clear(self):
        result = requests.post(f'{self._uri_}/{self._id_}')
        if result.status_code not in [200, 201]:
            raise ValueError(f'Cannot clear dictionary: {result.status_code}')

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self.__setitem__(k, v)

    def _keytransform(self, key):
        return key
