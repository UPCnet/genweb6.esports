# -*- coding: utf-8 -*-
"""get_XML: solo http(s), con timeout y sin resolver entidades externas."""
from unittest import mock

import importlib
import os
import tempfile
import unittest

# el modulo se llama "import", por lo que no se puede importar con "import"
sync = importlib.import_module('genweb6.esports.browser.import')


class FakeContext(object):

    def __init__(self, url):
        self.url = url


class FakeResponse(object):

    def __init__(self, content):
        self.content = content

    def raise_for_status(self):
        pass


def make_view(url):
    view = sync.ImporterView.__new__(sync.ImporterView)
    view.context = FakeContext(url)
    return view


class TestGetXML(unittest.TestCase):

    def test_non_http_url_is_rejected(self):
        for url in ('file:///etc/passwd', 'ftp://example.org/x.xml', '', None):
            view = make_view(url)
            with mock.patch.object(sync.requests, 'get') as get:
                with self.assertRaises(ValueError):
                    view.get_XML()
            get.assert_not_called()

    def test_request_has_timeout(self):
        view = make_view('https://example.org/data.xml')
        with mock.patch.object(sync.requests, 'get',
                               return_value=FakeResponse(b'<a><b>1</b></a>')) as get:
            view.get_XML()
        self.assertIn('timeout', get.call_args[1])
        self.assertEqual(view.xml.tag, 'a')

    def test_external_entities_are_not_resolved(self):
        secret = tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False)
        secret.write('SECRETO')
        secret.close()
        try:
            xml = ('<?xml version="1.0"?><!DOCTYPE a [<!ENTITY x SYSTEM "file://%s">]>'
                   '<a>&x;</a>' % secret.name).encode()
            view = make_view('https://example.org/data.xml')
            with mock.patch.object(sync.requests, 'get',
                                   return_value=FakeResponse(xml)):
                view.get_XML()
            self.assertNotIn('SECRETO', ''.join(view.xml.itertext()))
        finally:
            os.remove(secret.name)
