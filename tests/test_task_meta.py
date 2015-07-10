#!/usr/bin/env python
import unittest
from creo.task_meta import TaskRegisterMemento


class TaskTestCase(unittest.TestCase):

    def test_memento_single(self):
        class BaseObj(object):
            __metaclass__ = TaskRegisterMemento

            def __init__(self, *args, **kwargs):
                pass

        t1 = BaseObj()
        t2 = BaseObj()
        self.assertTrue(t1 is t2)
        self.assertFalse(t1 is not t2)

        t1 = BaseObj(a='b')
        t2 = BaseObj(a='b')
        self.assertTrue(t1 is t2)
        self.assertFalse(t1 is not t2)

        t1 = BaseObj(a='b', ab=[3, 5, 1], b=4, c={'a': 12, 'b': 123})
        t2 = BaseObj(c={'b': 123, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertTrue(t1 is t2)
        self.assertFalse(t1 is not t2)

        t2 = BaseObj(c={'b': 987, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertTrue(t1 is not t2)
        self.assertFalse(t1 is t2)

    def test_memento_two(self):
        class BaseObj(object):
            __metaclass__ = TaskRegisterMemento

            def __init__(self, *args, **kwargs):
                pass

        class SubObj1(BaseObj):
            pass

        class SubObj2(BaseObj):
            pass

        t1 = SubObj1()
        t2 = SubObj1()
        self.assertTrue(t1 is t2)
        self.assertFalse(t1 is not t2)

        t1 = SubObj1(a='b')
        t2 = SubObj2(a='b')
        self.assertTrue(t1 is not t2)
        self.assertFalse(t1 is t2)

        t1 = BaseObj(a='b', ab=[3, 5, 1], b=4, c={'a': 12, 'b': 123})
        t2 = BaseObj(c={'b': 123, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertTrue(t1 is t2)

        t2 = BaseObj(c={'b': 987, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertTrue(t1 is not t2)

    def test_register(self):
        class BaseObj(object):
            __metaclass__ = TaskRegisterMemento

        class SubObj1(BaseObj):
            pass

        class SubObj2(BaseObj):
            pass

        class SubObj3(BaseObj):
            pass

        class SubObj3_1(SubObj3):
            pass

        class SubObj4(BaseObj):
            pass

        print BaseObj.classes
        print len(BaseObj.classes)
        print BaseObj.instances
        self.assertEqual(len(BaseObj.instances), 0)

        print "\nCreating: SubObj1"
        SubObj1()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 6)
        self.assertEqual(len(BaseObj.instances), 1)

        print "\nCreating: SubObj2"
        SubObj2()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 6)
        self.assertEqual(len(BaseObj.instances), 2)

        print "\nCreating: SubObj2"
        SubObj2()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 6)
        self.assertEqual(len(BaseObj.instances), 2)

        print "\nCreating: SubObj3"
        SubObj3()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 6)
        self.assertEqual(len(SubObj3.classes), 6)
        self.assertEqual(len(BaseObj.instances), 3)
        self.assertEqual(len(SubObj3.instances), 3)

        print "\nCreating: SubObj4"
        SubObj4()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 6)
        self.assertEqual(len(BaseObj.instances), 4)

        print "\nCreating: SubObj3_1"
        SubObj3_1()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 6)
        self.assertEqual(len(BaseObj.instances), 5)
