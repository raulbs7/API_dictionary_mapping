#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import restdict

SERVER_ADDRESS = 'http://localhost:9001'
SERVER_API_URI = f'{SERVER_ADDRESS}/api/v1'

NON_STRING_VALUE = 0
TEST_KEY = 'test_key'
TEST_VALUE = 'test_value'
NEW_KEY = 'new_key'
NEW_VALUE = 'new_value'
ANOTHER_KEY = 'another_key'
ANOTHER_VALUE = 'another_value'
TEST_DICT = {NEW_KEY: NEW_VALUE, ANOTHER_KEY: ANOTHER_VALUE}


class TestIntegration(unittest.TestCase):
    '''
    Tests de integracion
    '''

    def test_check_empty(self):
        '''Un nuevo RestDict esta vacio y es del tipo correcto'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            self.assertIsInstance(test_dict, restdict.RestDict)
            self.assertEqual(len(test_dict), 0)

    def test_keyerror(self):
        '''Acceder con una key que no exista debe provocar una excepcion'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            with self.assertRaises(KeyError):
                test_dict[TEST_KEY]

    def test_invalid_key(self):
        '''Usar una key que no sea string debe provocar una excepcion'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            with self.assertRaises(TypeError):
                test_dict[NON_STRING_VALUE] = TEST_VALUE

    def test_store_and_get(self):
        '''Almacenar un nuevo valor incrementa la longitud del diccionario en uno (PUT/GET)'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            self.assertNotIn(TEST_KEY, test_dict)
            initial_size = len(test_dict)
            test_dict[TEST_KEY] = TEST_VALUE
            self.assertEqual(len(test_dict), initial_size + 1)
            self.assertIn(TEST_KEY, test_dict)
            self.assertEqual(test_dict[TEST_KEY], TEST_VALUE)

    def test_delete(self):
        '''Eliminar un elemento decrementa la longitug del diccionario'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            test_dict[TEST_KEY] = TEST_VALUE
            initial_size = len(test_dict)
            del test_dict[TEST_KEY]
            self.assertEqual(len(test_dict), initial_size - 1)
            self.assertNotIn(TEST_KEY, test_dict)

    def test_single_update(self):
        '''Modificar un elemento (POST)'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            test_dict[TEST_KEY] = TEST_VALUE
            test_dict[TEST_KEY] = NEW_VALUE
            self.assertEqual(len(test_dict), 1)
            self.assertIn(TEST_KEY, test_dict)
            self.assertEqual(test_dict[TEST_KEY], NEW_VALUE)

    def test_multi_update(self):
        '''Metodo update() de diccionarios'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            test_dict[TEST_KEY] = TEST_VALUE
            test_dict.update(TEST_DICT)
            self.assertEqual(len(test_dict), 1 + len(TEST_DICT))
            self.assertIn(TEST_KEY, test_dict)
            self.assertIn(NEW_KEY, test_dict)
            self.assertIn(ANOTHER_KEY, test_dict)
            self.assertEqual(test_dict[TEST_KEY], TEST_VALUE)
            self.assertEqual(test_dict[NEW_KEY], NEW_VALUE)
            self.assertEqual(test_dict[ANOTHER_KEY], ANOTHER_VALUE)

    def test_get(self):
        '''Metodo get() de diccionarios'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            value = test_dict.get(TEST_KEY, None)
            self.assertIsNone(value)
            test_dict[TEST_KEY] = TEST_VALUE
            value = test_dict.get(TEST_KEY, None)
            self.assertEqual(value, TEST_VALUE)

    def test_keys(self):
        '''Metodo keys() de diccionarios'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            test_dict[TEST_KEY] = TEST_VALUE
            test_dict[NEW_KEY] = NEW_VALUE

            self.assertIn(TEST_KEY, test_dict.keys())
            self.assertIn(NEW_KEY, test_dict.keys())

    def test_values(self):
        '''Metodo values() de diccionarios'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            test_dict[TEST_KEY] = TEST_VALUE
            test_dict[NEW_KEY] = NEW_VALUE

            self.assertIn(TEST_VALUE, test_dict.values())
            self.assertIn(NEW_VALUE, test_dict.values())

    def test_clear(self):
        '''Metodo clear() de diccionarios'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            test_dict[TEST_KEY] = TEST_VALUE
            test_dict[NEW_KEY] = NEW_VALUE

            test_dict.clear()

            self.assertNotIn(TEST_VALUE, test_dict.values())
            self.assertNotIn(NEW_VALUE, test_dict.values())
            self.assertEqual(len(test_dict), 0)