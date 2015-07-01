#!/usr/bin/env python
import gc
import mock
import unittest

from creo.target import Target
from creo import LocalDirectory, LocalFile


class TargetTestCase(unittest.TestCase):

    def test_init(self):
        t = Target()

    def test_exists(self):
        t = Target()
        self.assertRaises(NotImplementedError, t.exists)

    def test_last_modified(self):
        t = Target()
        self.assertRaises(NotImplementedError, t.last_modified)

    def test_repr(self):
        t = Target()
        self.assertEqual(repr(t), "Target({})")


class TargetLastModfifiedTestCase(unittest.TestCase):

    def setUp(self):
        self.t1 = Target()
        self.t1.last_modified = mock.MagicMock()
        self.t1.last_modified.return_value = 0

        self.t2 = Target()
        self.t2.last_modified = mock.MagicMock()
        self.t2.last_modified.return_value = 0

    def test_eq(self):
        self.t1.last_modified.return_value = 100.001
        self.t2.last_modified.return_value = 100.001
        self.assertTrue(self.t1 == self.t2)
        self.t2.last_modified.return_value = 100.002
        self.assertFalse(self.t1 == self.t2)
        self.t2.last_modified.return_value = 99.002
        self.assertFalse(self.t1 == self.t2)

    def test_ne(self):
        self.t1.last_modified.return_value = 100.001
        self.t2.last_modified.return_value = 100.001
        self.assertFalse(self.t1 != self.t2)
        self.t2.last_modified.return_value = 100.002
        self.assertTrue(self.t1 != self.t2)
        self.t2.last_modified.return_value = 99.002
        self.assertTrue(self.t1 != self.t2)

    def test_gt(self):
        self.t1.last_modified.return_value = 100.001
        self.t2.last_modified.return_value = 100.001
        self.assertFalse(self.t1 < self.t2)
        self.assertFalse(self.t2 < self.t1)
        self.t2.last_modified.return_value = 100.002
        self.assertTrue(self.t1 < self.t2)
        self.assertFalse(self.t2 < self.t1)
        self.t2.last_modified.return_value = 99.002
        self.assertFalse(self.t1 < self.t2)
        self.assertTrue(self.t2 < self.t1)

    def test_ge(self):
        self.t1.last_modified.return_value = 100.001
        self.t2.last_modified.return_value = 100.001
        self.assertTrue(self.t1 <= self.t2)
        self.assertTrue(self.t2 <= self.t1)
        self.t2.last_modified.return_value = 100.002
        self.assertTrue(self.t1 <= self.t2)
        self.assertFalse(self.t2 <= self.t1)
        self.t2.last_modified.return_value = 99.002
        self.assertFalse(self.t1 <= self.t2)
        self.assertTrue(self.t2 <= self.t1)

    def test_lt(self):
        self.t1.last_modified.return_value = 100.001
        self.t2.last_modified.return_value = 100.001
        self.assertFalse(self.t1 < self.t2)
        self.assertFalse(self.t2 < self.t1)
        self.t2.last_modified.return_value = 100.002
        self.assertTrue(self.t1 < self.t2)
        self.assertFalse(self.t2 < self.t1)
        self.t2.last_modified.return_value = 99.002
        self.assertFalse(self.t1 < self.t2)
        self.assertTrue(self.t2 < self.t1)

    def test_le(self):
        self.t1.last_modified.return_value = 100.001
        self.t2.last_modified.return_value = 100.001
        self.assertTrue(self.t1 <= self.t2)
        self.assertTrue(self.t2 <= self.t1)
        self.t2.last_modified.return_value = 100.002
        self.assertTrue(self.t1 <= self.t2)
        self.assertFalse(self.t2 <= self.t1)
        self.t2.last_modified.return_value = 99.002
        self.assertFalse(self.t1 <= self.t2)
        self.assertTrue(self.t2 <= self.t1)
