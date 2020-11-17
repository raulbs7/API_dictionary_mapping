#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import restdict

SERVER_ADDRESS = 'http://localhost:9001'
SERVER_API_URI = f'{SERVER_ADDRESS}/api/v1'

DICT_NAME = 'new_dict'
ANOTHER_DICT_NAME = 'another_dict'
TEST_KEY = 'test_key'
TEST_VALUE = 'test_value'
ANOTHER_VALUE = 'another_value'
NON_STRING_VALUE = 0

class TestMultiDict(unittest.TestCase):
    """
    Tests feature "Multidict"
    """
    def test_create(self):
        """Crear un diccionario RestDict nuevo"""
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            self.assertIsInstance(test_dict, restdict.RestDict)
            self.assertEqual(len(test_dict), 0)

    def test_create_with_name(self):
        """Crear un diccionario RestDict nuevo usando un nombre"""
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI, DICT_NAME)
            self.assertIsInstance(test_dict, restdict.RestDict)
            self.assertEqual(len(test_dict), 0)

    def test_str_dict(self):
        """Obtener string del dictionario"""
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI, DICT_NAME)
            self.assertEqual(str(test_dict), str(restdict.RestDict))
            self.assertEqual(len(test_dict), 0)

    def test_create_error(self):
        """Creación de un diccionario cuyo nombre ya está registrado"""
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI, DICT_NAME)
            with self.assertRaises(Exception):
                other_test_dict = restdict.new_client(SERVER_API_URI, DICT_NAME)

    def test_delete(self):
        '''Crear y destruir un RestDict'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI, DICT_NAME)
            del test_dict
            with self.assertRaises(Exception):
                test_dict[TEST_KEY] = TEST_VALUE

    def test_keyerror_dict(self):
        """Acceder con una key que no exista debe provocar una excepcion"""
        with restdict.new_server(SERVER_ADDRESS):
            with self.assertRaises(KeyError):
                test_dict = restdict.new_client(SERVER_API_URI, NON_STRING_VALUE)
