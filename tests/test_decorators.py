#!/usr/bin/env python
import os
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

        @Task(task1)
        def task2(s):
            global ran_order
            print "task2"
            ran_order.append('two')

        self.assertEqual(ran_order, ['one', 'two'])


def touch_or_create(filename):
    if os.path.exists(filename):
        os.utime(filename, None)
    else:
        file(filename, 'w')
