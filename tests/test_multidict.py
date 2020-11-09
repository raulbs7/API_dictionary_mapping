#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import unittest

import restdict

SERVER_ADDRESS = 'http://localhost:9001'
SERVER_API_URI = f'{SERVER_ADDRESS}/api/v1'

DICT_NAME = str(uuid.uuid4())


class TestMultiDict(unittest.TestCase):
    '''
    Tests feature "Multidict"
    '''
    def test_create(self):
        '''Crear un diccionario RestDict nuevo'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI)
            self.assertIsInstance(test_dict, restdict.RestDict)
            self.assertEqual(len(test_dict), 0)

    def test_create_with_name(self):
        '''Crear un diccionario RestDict nuevo usando un nombre'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI, DICT_NAME)
            self.assertIsInstance(test_dict, restdict.RestDict)
            self.assertEqual(len(test_dict), 0)

    def test_create_and_connect(self):
        '''Crear un diccionario RestDict nuevo y conectarse a el'''
        with restdict.new_server(SERVER_ADDRESS):
            restdict.new_client(SERVER_API_URI, DICT_NAME)
            same_test_dict = restdict.connect_restdict(SERVER_API_URI, DICT_NAME)            
            self.assertIsInstance(same_test_dict, restdict.RestDict)
            self.assertEqual(len(same_test_dict), 0)

    def test_bad_connect(self):
        '''Conectarse a un RestDict inexistente'''
        with restdict.new_server(SERVER_ADDRESS):
            with self.assertRaises(Exception):
                restdict.connect_restdict(SERVER_API_URI, DICT_NAME)

    """def test_delete(self):
        '''Crear y destruir un RestDict'''
        with restdict.new_server(SERVER_ADDRESS):
            test_dict = restdict.new_client(SERVER_API_URI, DICT_NAME)
            restdict.delete_restdict(SERVER_API_URI, DICT_NAME)
            with self.assertRaises(Exception):
                len(test_dict)

    def test_bad_delete(self):
        '''Destruir un RestDict inexistente'''
        with restdict.new_server(SERVER_ADDRESS):
            with self.assertRaises(Exception):
                restdict.delete_restdict(SERVER_API_URI, DICT_NAME)"""
