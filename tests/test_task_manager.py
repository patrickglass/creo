#!/usr/bin/env python
import unittest
import creo


class TaskManagerTestCase(unittest.TestCase):

    def setUp(self):
        class BaseObj(creo.Task):
            def outputs(self):
                return ['a']

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

        self.target_cls = SubObj3_1
        self.runner = creo.TaskManager()

    def test_init(self):
        o = creo.TaskManager()
        self.assertEqual(o.base_class, creo.Task)
        self.assertEqual(o.worker_type, creo.task_manager.Worker)
        self.assertEqual(o.worker_results, {})

        o = creo.TaskManager(task_base=self.target_cls)
        self.assertEqual(o.base_class, self.target_cls)
        self.assertEqual(o.worker_type, creo.task_manager.Worker)
        self.assertEqual(o.worker_results, {})

        class Worker2(creo.task_manager.Worker):
            pass

        o = creo.TaskManager(worker_type=Worker2)
        self.assertEqual(o.base_class, creo.Task)
        self.assertEqual(o.worker_type, Worker2)
        self.assertEqual(o.worker_results, {})

        o = creo.TaskManager(task_base=self.target_cls, worker_type=Worker2)
        self.assertEqual(o.base_class, self.target_cls)
        self.assertEqual(o.worker_type, Worker2)
        self.assertEqual(o.worker_results, {})

    def test_target_to_instance(self):

        orig = self.target_cls()

        # Pass in string name
        o1 = self.runner._target_to_instance('SubObj3_1')
        # pass in instance of class
        o2 = self.runner._target_to_instance(self.target_cls())
        # pass in class def
        o3 = self.runner._target_to_instance(self.target_cls)

        self.assertTrue(o1 is o2)
        self.assertTrue(o2 is o3)
        self.assertTrue(orig is o1)
        self.assertTrue(orig is o2)
        self.assertTrue(orig is o3)

    def test_get_tasks_no_target(self):

        tasks = self.runner._get_tasks(None)
        self.assertEqual(
            [x.name for x in tasks],
            [
                'BaseObj',
                'SubObj1',
                'SubObj2',
                'SubObj3',
                'SubObj3_1',
                'SubObj4'
            ])

    def test_get_tasks_target(self):

        tasks = self.runner._get_tasks('SubObj2')
        self.assertEqual(
            [x.name for x in tasks],
            [
                'BaseObj',
                'SubObj1',
                'SubObj2',
                'SubObj3',
                'SubObj3_1',
                'SubObj4'
            ])
