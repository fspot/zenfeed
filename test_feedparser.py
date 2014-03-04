#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function, unicode_literals
import unittest

class TestFonctionGet(unittest.TestCase):
 
    def setUp(self):
        print('Setup !')
 
    def tearDown(self):
        print('Teardown !')
 
    def test_get_element(self):
        self.assertEqual('Oui', 'Je tres clair, Luc')

