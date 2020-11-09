#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import string
import unittest

import restdict

SERVER_ADDRESS = 'http://localhost:9001'
SERVER_API_URI = f'{SERVER_ADDRESS}/api/v1'

STRESS_OPERATIONS = 1000

STORE = 'store'
DELETE = 'delete'
UPDATE = 'update'

def random_string(length=10):
    chars = string.digits + string.ascii_letters
    return ''.join(random.choice(chars) for i in range(length))

def random_integer(min_int=0, max_int=sys.maxsize):
    return random.randint(min_int, max_int)

def ramdom_float():
    return random.random() * float(random_integer())

def random_builtin_value():
    return random.choice([None, True, False])

def random_basic_value():
    return random.choice([random_string(), random_integer(), ramdom_float(), random_builtin_value()])

def random_list(max_size=100):
    the_list = []
    for count in range(random_integer(1, max_size)):
        the_list.append(random_basic_value)
    return the_list

def random_dict(max_keys=100):
    the_dict = {}
    for count in range(random_integer(1, max_keys)):
        the_dict[random_string()] = random_basic_value()
    return the_dict

def random_value():
    return random.choice([random_basic_value(), random_list(), random_dict()])

def random_operation(dict1, dict2):
    OPERATIONS = [STORE]
    if (len(dict1) > 0) and (len(dict2) > 0):
        OPERATIONS += [DELETE, UPDATE]
    op = random.choice(OPERATIONS)
    if op == STORE:
        random_key = random_string(random.randint(2, 10))
        value = random_value()
        dict1[random_key] = value
        dict2[random_key] = value

    elif op == UPDATE:
        key = random.choice(dict1.keys())
        new_value = random_value()
        dict1[key] = new_value
        dict2[key] = new_value

    elif op == DELETE:
        key = random.choice(dict1.keys())
        del dict1[key]
        del dict2[key]

class TestStress(unittest.TestCase):
    '''
    Tests de integracion
    '''
    def setUp(self):
        self._server_ = restdict.new_server(SERVER_ADDRESS)
        self._server_.start()

        self._test_dict_ = restdict.new_client(SERVER_API_URI)
        self._normal_dict_ = {}

    def tearDown(self):
        self._server_.stop()

    def test_stress(self):
        for count in range(STRESS_OPERATIONS):
            random_operation(self._test_dict_, self._normal_dict_)
        self.assertListEqual(
            list(self._test_dict_.keys()), list(self._normal_dict_.keys())
        )
        for k in self._test_dict_:
            value = self._test_dict_[k]
            if isinstance(value, list):
                self.assertListEqual(value, self._normal_dict_[k])
            elif isinstance(value, dict):
                self.assertDictEqual(value, self._normal_dict_[k])
            else:
                self.assertEqual(value, self._normal_dict_[k])
