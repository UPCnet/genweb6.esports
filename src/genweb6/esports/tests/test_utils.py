# -*- coding: utf-8 -*-
"""get_list_from_string no debe ejecutar el contenido de los campos."""
from genweb6.esports.utils import get_list_from_string

import os
import tempfile
import unittest


class TestGetListFromString(unittest.TestCase):

    def test_list(self):
        self.assertEqual(get_list_from_string("['a', 'b']"), ['a', 'b'])

    def test_list_of_dicts(self):
        value = "[{'name': 'Tarifa', 'price': 10, 'tags': ('x',)}]"
        self.assertEqual(
            get_list_from_string(value),
            [{'name': 'Tarifa', 'price': 10, 'tags': ('x',)}])

    def test_invalid_returns_empty_list(self):
        self.assertEqual(get_list_from_string('no es una lista'), [])
        self.assertEqual(get_list_from_string(None), [])

    def test_code_is_not_executed(self):
        marker = os.path.join(tempfile.gettempdir(), 'genweb6_esports_eval_test')
        if os.path.exists(marker):
            os.remove(marker)
        payload = "__import__('os').system('touch %s')" % marker
        self.assertEqual(get_list_from_string(payload), [])
        self.assertFalse(os.path.exists(marker))
