#!/usr/bin/env python

import unittest
from creo import *

class TestDecorators(unittest.TestCase):

    def test_1(self):
        ran_order = list()
        ran_order.append('test')

        def task1():
            global ran_order
            print "task1"
            ran_order.append('one')
            print ran_order

        @follows('one')
        def task2():
            global ran_order
            print "task2"
            ran_order.append('two')

        # self.assertEqual(ran_order, ['one', 'two'])