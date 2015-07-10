#!/usr/bin/env python
import mock
import unittest

from creo import Reference, LocalDirectory, LocalFile, ConfigEntry


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


class LocalDirectoryLastModfifiedTestCase(ReferenceLastModfifiedTestCase):

    def setUp(self):
        self.t1 = LocalDirectory('.')
        self.t1.last_modified = mock.MagicMock()
        self.t1.last_modified.return_value = 0

        self.t2 = LocalDirectory('.')
        self.t2.last_modified = mock.MagicMock()
        self.t2.last_modified.return_value = 0


class LocalFileLastModfifiedTestCase(ReferenceLastModfifiedTestCase):

    def setUp(self):
        self.t1 = LocalFile('tmp_filename.txt')
        self.t1.last_modified = mock.MagicMock()
        self.t1.last_modified.return_value = 0

        self.t2 = LocalFile('tmp_filename.txt')
        self.t2.last_modified = mock.MagicMock()
        self.t2.last_modified.return_value = 0


class CommonFilesystemTestCase(unittest.TestCase):

    def setUp(self):
        self.file = '.'
        self.cls = LocalDirectory
        self.r = self.cls(self.file)

    @mock.patch.object(LocalDirectory, 'mkdir')
    def test_init_create(self, mock_method):
        self.r = self.cls(self.file, create=True)
        mock_method.assert_called_once_with()

        self.r = self.cls(self.file, True)
        mock_method.assert_called_with()

    @mock.patch.object(LocalDirectory, 'mkdir')
    def test_init_not_create(self, mock_method):
        self.r = self.cls(self.file, create=False)
        self.assertFalse(mock_method.called)

        self.r = self.cls(self.file, False)
        self.assertFalse(mock_method.called)

    @mock.patch('os.makedirs')
    @mock.patch('os.path.exists')
    def test_mkdir_exists(self, mock_exists, mock_makedirs):
        mock_exists.return_value = True
        self.r.mkdir()
        mock_exists.assert_called_once_with(self.r.directory)
        self.assertFalse(mock_makedirs.called)

    @mock.patch('os.makedirs')
    @mock.patch('os.path.exists')
    def test_mkdir_not_exists(self, mock_exists, mock_makedirs):
        mock_exists.return_value = False
        self.r.mkdir()
        mock_exists.assert_called_once_with(self.r.directory)
        mock_makedirs.assert_called_once_with(self.r.directory)

    @mock.patch('os.path.exists')
    def test_exists(self, mock_method):
        self.r.exists()
        mock_method.assert_called_once_with(self.file)

    def test_last_modified_not_exists(self):
        self.r.exists = mock.MagicMock()
        self.r.exists.return_value = False
        self.assertRaises(IOError, self.r.last_modified)

    def test_to_string_file_exists(self):
        self.r.last_modified = mock.MagicMock()
        self.r.last_modified.return_value = 11236981273
        self.assertEqual(
            self.r.to_string(),
            "%s: %-35s\t2326-02-01 07:41:13.000000" % (
                self.r.__class__.__name__, self.r.file))

    def test_to_string_file_not_exists(self):
        self.r.last_modified = mock.MagicMock()
        self.r.last_modified.side_effect = IOError()
        self.assertEqual(
            self.r.to_string(),
            "%s: %-35s\t<-- MISSING" % (
                self.r.__class__.__name__, self.r.file))

    def test_to_string_file_exists_verbose_multiline(self):
        self.r.last_modified = mock.MagicMock()
        self.r.last_modified.return_value = 11236981273
        self.assertEqual(
            self.r.to_string(compact=False),
            "%s: %s\n\tModified: 2326-02-01 07:41:13.000000" % (
                self.r.__class__.__name__, self.r.file))

    def test_to_string_file_not_exists_verbose_multiline(self):
        self.r.last_modified = mock.MagicMock()
        self.r.last_modified.side_effect = IOError()
        self.assertEqual(
            self.r.to_string(compact=False),
            "%s: %s\n\tModified: <-- MISSING" % (
                self.r.__class__.__name__, self.r.file))

    def test__str__(self):
        self.assertEqual(str(self.r), self.file)


class LocalDirectoryFilesystemTestCase(CommonFilesystemTestCase):

    def setUp(self):
        self.file = '.'
        self.cls = LocalDirectory
        self.r = self.cls(self.file)

    @mock.patch('os.stat')
    def test_last_modified_exists(self, mock_method):
        self.r.exists = mock.MagicMock()
        mock_method.return_value.st_mtime = 11236981273
        val = self.r.last_modified()
        mock_method.assert_called_once_with(self.r.file)
        self.assertEqual(val, 11236981273)


class LocalFileFilesystemTestCase(CommonFilesystemTestCase):

    def setUp(self):
        self.file = 'tmp_filename.txt'
        self.cls = LocalFile
        self.r = self.cls(self.file)

    @mock.patch('os.path.getmtime')
    def test_last_modified_exists(self, mock_method):
        self.r.exists = mock.MagicMock()
        mock_method.return_value = 11236981273
        val = self.r.last_modified()
        mock_method.assert_called_once_with(self.r.file)
        self.assertEqual(val, 11236981273)

    @mock.patch('os.utime')
    def test_touch(self, mock_method):
        timestamp = None
        m = mock.mock_open()
        with mock.patch('__builtin__.open', m, create=True):
            self.r.touch(timestamp)
        mock_method.assert_called_once_with(self.r.file, timestamp)
        m.assert_called_once_with(self.r.file, 'a')

    def test_open(self):
        mode = 'w'
        m = mock.mock_open()
        with mock.patch('__builtin__.open', m, create=True):
            self.r.open(mode)
        m.assert_called_once_with(self.r.file, mode)


class ConfigEntryTestCase(unittest.TestCase):

    def setUp(self):
        self.cls = ConfigEntry
        self.key = 'keyname'
        self.env = mock.MagicMock()

        self.r = self.cls(self.key, self.env)

    def test_init(self):
        self.assertRaises(TypeError, self.cls)
        self.assertTrue(self.cls(self.key))
        self.assertTrue(self.cls(self.key, self.env))

    def test_set(self):
        val = 'myvalue'
        self.r.set(val)
        self.env.set.assert_called_once_with(self.key, val)
        val = 123
        self.r.set(val)
        self.env.set.assert_called_with(self.key, val)

    def test_get(self):
        self.r.get()
        self.env.get.assert_called_once_with(self.key, None)
        self.r.get(default=2342)
        self.env.get.assert_called_with(self.key, 2342)
        self.r.get('mydefault')
        self.env.get.assert_called_with(self.key, 'mydefault')

    def test_last_modified(self):
        mod_time = 11236981273
        self.env.last_modified.return_value = mod_time

        val = self.r.last_modified()
        self.env.last_modified.assert_called_once_with(self.key)
        self.assertEqual(val, mod_time)

    def test_exists(self):
        self.env.get.return_value = 'notNoneValue'
        val = self.r.exists()
        self.assertTrue(val)
        self.env.get.assert_called_once_with(self.key)

        self.env.get.return_value = 1234
        val = self.r.exists()
        self.assertTrue(val)
        self.env.get.assert_called_with(self.key)

    def test_not_exists(self):
        self.env.get.return_value = None
        val = self.r.exists()
        self.assertFalse(val)
        self.env.get.assert_called_once_with(self.key)
