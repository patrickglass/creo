#!/usr/bin/env python
import unittest
from creo.task_meta import TaskRegisterMemento


class TaskTestCase(unittest.TestCase):

    def test_memento_single(self):
        class BaseObj(object):
            __metaclass__ = TaskRegisterMemento

            def __init__(self, *args, **kwargs):
                pass

        self.assertEqual(len(BaseObj.instance_cache), 0)
        t1 = BaseObj()
        self.assertEqual(len(BaseObj.instance_cache), 1)
        t2 = BaseObj()
        self.assertEqual(len(BaseObj.instance_cache), 1)
        self.assertTrue(t1 is t2)
        self.assertFalse(t1 is not t2)

        t1 = BaseObj(a='b')
        self.assertEqual(len(BaseObj.instance_cache), 2)
        t2 = BaseObj(a='b')
        self.assertEqual(len(BaseObj.instance_cache), 2)
        self.assertTrue(t1 is t2)
        self.assertFalse(t1 is not t2)

        t1 = BaseObj(a='b', ab=[3, 5, 1], b=4, c={'a': 12, 'b': 123})
        self.assertEqual(len(BaseObj.instance_cache), 3)
        t2 = BaseObj(c={'b': 123, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertEqual(len(BaseObj.instance_cache), 3)
        self.assertTrue(t1 is t2)
        self.assertFalse(t1 is not t2)

        t2 = BaseObj(c={'b': 987, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertEqual(len(BaseObj.instance_cache), 4)
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

        self.assertEqual(len(BaseObj.instance_cache), 0)
        t1 = SubObj1()
        self.assertEqual(len(BaseObj.instance_cache), 1)
        t2 = SubObj1()
        self.assertEqual(len(BaseObj.instance_cache), 1)
        self.assertTrue(t1 is t2)
        self.assertFalse(t1 is not t2)

        t1 = SubObj1(a='b')
        self.assertEqual(len(BaseObj.instance_cache), 2)
        t2 = SubObj2(a='b')
        self.assertEqual(len(BaseObj.instance_cache), 3)
        self.assertTrue(t1 is not t2)
        self.assertFalse(t1 is t2)

        t1 = BaseObj(a='b', ab=[3, 5, 1], b=4, c={'a': 12, 'b': 123})
        self.assertEqual(len(BaseObj.instance_cache), 4)
        t2 = BaseObj(c={'b': 123, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertEqual(len(BaseObj.instance_cache), 4)
        self.assertTrue(t1 is t2)

        t2 = BaseObj(c={'b': 987, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertEqual(len(BaseObj.instance_cache), 5)
        self.assertTrue(t1 is not t2)

    def test_memento_isolate(self):
        class BaseObj(object):
            __metaclass__ = TaskRegisterMemento

            def __init__(self, *args, **kwargs):
                pass

        class SubObj1(BaseObj):
            pass

        class SubObj2(BaseObj):
            pass

        class BaseObj2(object):
            __metaclass__ = TaskRegisterMemento

            def __init__(self, *args, **kwargs):
                pass

        class SubObj3(BaseObj2):
            pass

        class SubObj4(BaseObj2):
            pass

        # # BaseObj1
        self.assertEqual(len(BaseObj.instance_cache), 0)
        t1 = SubObj1()
        self.assertEqual(len(BaseObj.instance_cache), 1)
        t2 = SubObj1()
        self.assertEqual(len(BaseObj.instance_cache), 1)
        self.assertTrue(t1 is t2)
        self.assertFalse(t1 is not t2)

        t1 = SubObj1(a='b')
        self.assertEqual(len(BaseObj.instance_cache), 2)
        t2 = SubObj2(a='b')
        self.assertEqual(len(BaseObj.instance_cache), 3)
        self.assertTrue(t1 is not t2)
        self.assertFalse(t1 is t2)

        t1 = BaseObj(a='b', ab=[3, 5, 1], b=4, c={'a': 12, 'b': 123})
        self.assertEqual(len(BaseObj.instance_cache), 4)
        t2 = BaseObj(c={'b': 123, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertEqual(len(BaseObj.instance_cache), 4)
        self.assertTrue(t1 is t2)

        t2 = BaseObj(c={'b': 987, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertEqual(len(BaseObj.instance_cache), 5)
        self.assertTrue(t1 is not t2)

        # # BaseObj2
        self.assertEqual(len(BaseObj2.instance_cache), 0)
        t1 = SubObj3()
        self.assertEqual(len(BaseObj2.instance_cache), 1)
        t2 = SubObj3()
        self.assertEqual(len(BaseObj2.instance_cache), 1)
        self.assertTrue(t1 is t2)
        self.assertFalse(t1 is not t2)

        t1 = SubObj3(a='b')
        self.assertEqual(len(BaseObj2.instance_cache), 2)
        t2 = SubObj4(a='b')
        self.assertEqual(len(BaseObj2.instance_cache), 3)
        self.assertTrue(t1 is not t2)
        self.assertFalse(t1 is t2)

        t1 = BaseObj2(a='b', ab=[3, 5, 1], b=4, c={'a': 12, 'b': 123})
        self.assertEqual(len(BaseObj2.instance_cache), 4)
        t2 = BaseObj2(c={'b': 123, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertEqual(len(BaseObj2.instance_cache), 4)
        self.assertTrue(t1 is t2)

        t2 = BaseObj2(c={'b': 987, 'a': 12}, a='b', ab=[3, 5, 1], b=4)
        self.assertEqual(len(BaseObj2.instance_cache), 5)
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
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(BaseObj.instances), 1)

        print "\nCreating: SubObj2"
        SubObj2()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(BaseObj.instances), 2)

        print "\nCreating: SubObj2"
        SubObj2()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(BaseObj.instances), 2)

        print "\nCreating: SubObj3"
        SubObj3()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(SubObj3.classes), 5)
        self.assertEqual(len(BaseObj.instances), 3)
        self.assertEqual(len(SubObj3.instances), 3)

        print "\nCreating: SubObj4"
        SubObj4()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(BaseObj.instances), 4)

        print "\nCreating: SubObj3_1"
        SubObj3_1()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(BaseObj.instances), 5)

    def test_register_isolate(self):
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

        class BaseObj2(object):
            __metaclass__ = TaskRegisterMemento

        class SubObj5(BaseObj2):
            pass

        class SubObj6(BaseObj2):
            pass

        class SubObj7(BaseObj2):
            pass

        class SubObj7_1(SubObj7):
            pass

        class SubObj8(BaseObj2):
            pass

        # # BaseObj
        print BaseObj.classes
        print len(BaseObj.classes)
        print BaseObj.instances
        self.assertEqual(len(BaseObj.instances), 0)

        print "\nCreating: SubObj1"
        SubObj1()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(BaseObj.instances), 1)

        print "\nCreating: SubObj2"
        SubObj2()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(BaseObj.instances), 2)

        print "\nCreating: SubObj2"
        SubObj2()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(BaseObj.instances), 2)

        print "\nCreating: SubObj3"
        SubObj3()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(SubObj3.classes), 5)
        self.assertEqual(len(BaseObj.instances), 3)
        self.assertEqual(len(SubObj3.instances), 3)

        print "\nCreating: SubObj4"
        SubObj4()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(BaseObj.instances), 4)

        print "\nCreating: SubObj3_1"
        SubObj3_1()
        print BaseObj.classes
        self.assertEqual(len(BaseObj.classes), 5)
        self.assertEqual(len(BaseObj.instances), 5)

        # # BaseObj2
        print BaseObj2.classes
        print len(BaseObj2.classes)
        print BaseObj2.instances
        self.assertEqual(len(BaseObj2.instances), 0)

        print "\nCreating: SubObj5"
        SubObj5()
        print BaseObj2.classes
        self.assertEqual(len(BaseObj2.classes), 5)
        self.assertEqual(len(BaseObj2.instances), 1)

        print "\nCreating: SubObj6"
        SubObj6()
        print BaseObj2.classes
        self.assertEqual(len(BaseObj2.classes), 5)
        self.assertEqual(len(BaseObj2.instances), 2)

        print "\nCreating: SubObj6"
        SubObj6()
        print BaseObj2.classes
        self.assertEqual(len(BaseObj2.classes), 5)
        self.assertEqual(len(BaseObj2.instances), 2)

        print "\nCreating: SubObj7"
        SubObj7()
        print BaseObj2.classes
        self.assertEqual(len(BaseObj2.classes), 5)
        self.assertEqual(len(SubObj7.classes), 5)
        self.assertEqual(len(BaseObj2.instances), 3)
        self.assertEqual(len(SubObj7.instances), 3)

        print "\nCreating: SubObj8"
        SubObj8()
        print BaseObj2.classes
        self.assertEqual(len(BaseObj2.classes), 5)
        self.assertEqual(len(BaseObj2.instances), 4)

        print "\nCreating: SubObj7_1"
        SubObj7_1()
        print BaseObj2.classes
        self.assertEqual(len(BaseObj2.classes), 5)
        self.assertEqual(len(BaseObj2.instances), 5)

    def test_class_by_name(self):
        class BaseObj(object):
            __metaclass__ = TaskRegisterMemento

        class SubObj1(BaseObj):
            pass

        class SubObj3(BaseObj):
            pass

        self.assertEqual(SubObj1.class_by_name('SubObj1').__name__, 'SubObj1')
