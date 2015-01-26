#!/usr/bin/env python
import gc
import unittest
from creo import Task

class TestTaskInstanceCreate(unittest.TestCase):

    def test_create_no_tasks(self):
        i = 0
        for obj in Task.getinstances():
            print obj.name
            i += 1
        self.assertEqual(i, 0)

    def test_create_tasks(self):
        i = 0
        t1 = Task()
        t2 = Task()
        t3 = Task()

        for obj in Task.getinstances():
            print obj.name
            i += 1
        self.assertEqual(i, 3)

    def test_create_tasks_delete(self):
        i = 0
        t11 = Task()
        t21 = Task()
        t31 = Task()
        print len(Task.getinstances())
        for obj in Task.getinstances():
            print obj.name
            i += 1
        self.assertEqual(i, 3)

        i = 0
        del t31
        print "GC Collected: ", gc.collect()
        for obj in Task.getinstances():
            print obj.name
            i += 1
        print len(Task.getinstances())
        self.assertEqual(i, 2)
        print len(Task.getinstances())

        i = 0
        del t21
        print "GC Collected: ", gc.collect()
        print len(Task.getinstances())
        for obj in Task.getinstances():
            print obj.name
            i += 1
        print len(Task.getinstances())
        self.assertEqual(i, 1)
        print len(Task.getinstances())

    def test_create_tasks_delete1(self):
        i = 0
        t1 = Task()
        t2 = Task()
        t3 = Task()
        t4 = Task()

        self.assertEqual(len(Task.getinstances()), 4)
        del t1
        self.assertEqual(len(Task.getinstances()), 3)

    def test_create_tasks_delete2(self):
        i = 0
        t1 = Task()
        t2 = Task()
        t3 = Task()
        t4 = Task()

        self.assertEqual(len(Task.getinstances()), 4)
        del t1
        del t3
        self.assertEqual(len(Task.getinstances()), 2)

    def test_create_tasks_delete3(self):
        i = 0
        t1 = Task()
        t2 = Task()
        t3 = Task()
        t4 = Task()

        self.assertEqual(len(Task.getinstances()), 4)
        del t1
        del t3
        del t2
        self.assertEqual(len(Task.getinstances()), 1)

    def test_create_tasks_delete3None(self):
        i = 0
        t1 = Task()
        t2 = Task()
        t3 = Task()
        t4 = Task()

        self.assertEqual(len(Task.getinstances()), 4)
        t1 = None
        t3 = None
        t2 = None
        self.assertEqual(len(Task.getinstances()), 1)

    def test_create_tasks_delete4(self):
        i = 0
        t1 = Task()
        t2 = Task()
        t3 = Task()
        t4 = Task()

        self.assertEqual(len(Task.getinstances()), 4)
        del t1
        del t3
        del t2
        del t4
        self.assertEqual(len(Task.getinstances()), 0)
