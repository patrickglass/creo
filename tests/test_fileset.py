#!/usr/bin/env python
"""
Module test_fileset

:Company: PMC-Sierra Inc.
:Author: Patrick Glass <patrick.glass@pmcs.com>
:Copyright: Copyright 2013 PMC-Sierra, Inc.

UnitTest framework for validating the PMCX system
"""
import sys
import os
import re
import time
import unittest

from creo.dependancy import FileSetDep as FileSet


def touch_files(filelist, incr=10):
    t = time.time()
    for f in filelist:
        open(f, 'w').close()
        times = (t, t)
        os.utime(f, times)
        # Each file timestamp get incremented by
        # incr number of milliseconds
        t = t + incr


class TestCaseEmptyArgs(unittest.TestCase):

    def test_glob_no_args(self):
        self.assertRaises(ValueError, FileSet)

    def test_glob_empty_str(self):
        self.assertTrue(FileSet(''))

    def test_glob_no_pattern_entered(self):
        self.assertTrue(FileSet(''))
        self.assertTrue(FileSet('a'))


# class TestCaseMissingFiles(unittest.TestCase):

#     def test_glob_missing_file(self):
#         self.assertRaises(ValueError, FileSet, 'filemissing.badfile')

#     def test_glob_missing_file_many(self):
#         self.assertRaises(ValueError, FileSet, 'filemissing.badfile', 'filemissing.badfile2')

#     def test_glob_missing_file_many2(self):
#         self.assertRaises(ValueError, FileSet, 'f.nofile', 'abc.nofile1', 'abc.nofile2')

#     def test_glob_missing_file_list(self):
#         self.assertRaises(ValueError, FileSet, ['f.nofile', 'abc.nofile1', 'abc.nofile2'])


class TestCaseSingleSeriesIteratingOrdered(unittest.TestCase):

    def setUp(self):
        self.file_list = ['1_1', '2_1']
        touch_files(self.file_list)
        self.one = FileSet('1_*')
        self.two = FileSet('2_*')

    def tearDown(self):
        for file_name in self.file_list:
            os.remove(file_name)

    def test_greater_than(self):
        self.assertTrue(self.two > self.one)
        self.assertGreater(self.two, self.one)
        self.assertGreaterEqual(self.two, self.one)

    def test_not_greater_than(self):
        self.assertFalse(self.one > self.two)
        self.assertLess(self.one, self.two)
        self.assertLessEqual(self.one, self.two)

    def test_less_than(self):
        self.assertTrue(self.one < self.two)
        self.assertLess(self.one, self.two)
        self.assertLessEqual(self.one, self.two)

    def test_not_less_than(self):
        self.assertFalse(self.two < self.one)
        self.assertGreater(self.two, self.one)
        self.assertGreaterEqual(self.two, self.one)

    def test_equals(self):
        self.assertTrue(self.two != self.one)
        self.assertTrue(self.one != self.two)

    def test_not_equals(self):
        self.assertFalse(self.two == self.one)
        self.assertFalse(self.one == self.two)

    def test_to_string(self):
        self.assertTrue(re.match("Dependancy: from \[.*\] to \[.*\]:\n\t1_1", str(self.one)))


class TestCaseMultipleSeriesIteratingOrdered(unittest.TestCase):

    def setUp(self):
        self.file_list = ['1_1', '1_2', '2_1', '2_2']
        touch_files(self.file_list)
        self.one = FileSet('1_*')
        self.two = FileSet('2_*')

    def tearDown(self):
        for file_name in self.file_list:
            os.remove(file_name)

    def test_greater_than(self):
        self.assertTrue(self.two > self.one)
        self.assertGreater(self.two, self.one)
        self.assertGreaterEqual(self.two, self.one)

    def test_not_greater_than(self):
        self.assertFalse(self.one > self.two)

    def test_less_than(self):
        self.assertTrue(self.one < self.two)

    def test_not_less_than(self):
        self.assertFalse(self.two < self.one)


class TestCaseMultipleSeriesIteratingOrderedNoWildcardsOneMissing(unittest.TestCase):

    def setUp(self):
        self.file_list = ['1_1', '1_2', '2_1', '2_2']
        touch_files(self.file_list)
        self.one = FileSet('1_1', '1_2', '1_3')
        self.two = FileSet('2_1', '2_2')

    def tearDown(self):
        for file_name in self.file_list:
            os.remove(file_name)

    def test_greater_than(self):
        self.assertTrue(self.two > self.one)
        self.assertGreater(self.two, self.one)
        self.assertGreaterEqual(self.two, self.one)

    def test_not_greater_than(self):
        self.assertFalse(self.one > self.two)

    def test_less_than(self):
        self.assertTrue(self.one < self.two)

    def test_not_less_than(self):
        self.assertFalse(self.two < self.one)

    # def test_not_eq(self):
    #     self.assertFalse(self.two == self.one)


class TestCaseMultipleSeriesIteratingShuffled(unittest.TestCase):

    def setUp(self):
        self.file_list = ['1_1', '2_1', '1_2', '2_2']
        touch_files(self.file_list)
        self.one = FileSet('1_*')
        self.two = FileSet('2_*')

    def tearDown(self):
        for file_name in self.file_list:
            os.remove(file_name)

    def test_not_greater_than(self):
        self.assertFalse(self.two > self.one)

    def test_not_greater_than2(self):
        self.assertFalse(self.one > self.two)

    def test_not_less_than(self):
        self.assertFalse(self.one < self.two)

    def test_not_less_than2(self):
        self.assertFalse(self.two < self.one)

    # def test_not_eq(self):
    #     self.assertFalse(self.two == self.one)


class TestCaseMultipleSeriesIteratingShuffled2(unittest.TestCase):

    def setUp(self):
        self.file_list = ['2_1', '1_2', '1_1', '2_2']
        touch_files(self.file_list, incr=0)
        self.one = FileSet('1_*')
        self.two = FileSet('2_*')

    def tearDown(self):
        for file_name in self.file_list:
            os.remove(file_name)

    def test_not_greater_than1(self):
        self.assertFalse(self.two > self.one)

    def test_not_greater_than2(self):
        self.assertFalse(self.one > self.two)

    def test_not_less_than1(self):
        self.assertFalse(self.one < self.two)

    def test_not_less_than2(self):
        self.assertFalse(self.two < self.one)

    # def test_eq(self):
    #     self.assertTrue(self.two == self.one)


class TestCaseMultipleSeriesAllEqual(unittest.TestCase):

    def setUp(self):
        self.file_list = ['1_1', '1_2', '2_1', '2_2']
        touch_files(self.file_list, incr=0)
        self.one = FileSet('1_*')
        self.two = FileSet('2_*')

    def tearDown(self):
        for file_name in self.file_list:
            os.remove(file_name)

    def test_not_greater_than1(self):
        self.assertFalse(self.two > self.one)

    def test_not_greater_than2(self):
        self.assertFalse(self.one > self.two)

    def test_not_less_than1(self):
        self.assertFalse(self.one < self.two)

    def test_not_less_than2(self):
        self.assertFalse(self.two < self.one)

    # def test_eq(self):
    #     self.assertTrue(self.two == self.one)


class TestCaseThreeSetMultipleSeriesIteratingOrdered(unittest.TestCase):

    def setUp(self):
        self.file_list = ['1_1', '1_2', '2_1', '2_2', '3_1', '3_2']
        touch_files(self.file_list)
        self.one = FileSet('1_*')
        self.two = FileSet('2_*')
        self.three = FileSet('3_*')

    def tearDown(self):
        for file_name in self.file_list:
            os.remove(file_name)

    def test_greater_than_with_3_objects(self):
        self.assertTrue(self.three > self.two > self.one)

    def test_greater_than_bool_fileset_comparison(self):
        self.assertRaises(AttributeError, eval, '(self.three > self.two) > self.one')

    def test_less_than_bool_fileset_comparison(self):
        self.assertRaises(AttributeError, eval, '(self.three < self.two) < self.one')

    def test_not_greater_than_with_3_objects(self):
        self.assertFalse(self.two > self.one > self.three)


class TestCaseMutiGlobOrdered(unittest.TestCase):

    def setUp(self):
        self.file_list = ['1_1', '1_2', '2_1', '2_2', '3_1', '3_2']
        touch_files(self.file_list)
        self.one = FileSet('1_*', '2_*')
        self.two = FileSet('3_*')

    def tearDown(self):
        for file_name in self.file_list:
            os.remove(file_name)

    def test_greater_than(self):
        self.assertTrue(self.two > self.one)
        self.assertGreater(self.two, self.one)
        self.assertGreaterEqual(self.two, self.one)

    def test_not_greater_than(self):
        self.assertFalse(self.one > self.two)
        self.assertLess(self.one, self.two)
        self.assertLessEqual(self.one, self.two)

    def test_less_than(self):
        self.assertTrue(self.one < self.two)
        self.assertLess(self.one, self.two)
        self.assertLessEqual(self.one, self.two)

    def test_not_less_than(self):
        self.assertFalse(self.two < self.one)
        self.assertGreater(self.two, self.one)
        self.assertGreaterEqual(self.two, self.one)

    def test_not_equals(self):
        self.assertFalse(self.two == self.one)


class TestCaseMutiGlobOrderedShuffled(unittest.TestCase):

    def setUp(self):
        self.file_list = ['1_1', '1_2', '2_1', '2_2', '3_1', '3_2']
        touch_files(self.file_list)
        self.one = FileSet('1_1', '1_2', '2_1')
        self.two = FileSet('1_2', '2_2', '3_1', '3_2')

    def tearDown(self):
        for file_name in self.file_list:
            os.remove(file_name)

    def test_greater_than(self):
        self.assertFalse(self.two > self.one)
        self.assertFalse(self.two >= self.one)
        self.assertFalse(self.one > self.two)
        self.assertFalse(self.one >= self.two)

    def test_less_than(self):
        self.assertFalse(self.two < self.one)
        self.assertFalse(self.two <= self.one)
        self.assertFalse(self.one < self.two)
        self.assertFalse(self.one <= self.two)

    def test_equals(self):
        self.assertFalse(self.two == self.one)
        self.assertFalse(self.one == self.two)


if __name__ == '__main__':
    print "INFO: Running tests for fileset class!"
    unittest.main()

