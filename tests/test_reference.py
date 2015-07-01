#!/usr/bin/env python
import mock
import unittest

from creo import Reference


class ReferenceTestCase(unittest.TestCase):

    def test_init(self):
        Reference()

    def test_exists(self):
        t = Reference()
        self.assertRaises(NotImplementedError, t.exists)

    def test_last_modified(self):
        t = Reference()
        self.assertRaises(NotImplementedError, t.last_modified)

    def test_repr(self):
        t = Reference()
        self.assertEqual(repr(t), "Reference({})")


class ReferenceLastModfifiedTestCase(unittest.TestCase):

    def setUp(self):
        self.t1 = Reference()
        self.t1.last_modified = mock.MagicMock()
        self.t1.last_modified.return_value = 0

        self.t2 = Reference()
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
