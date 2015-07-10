#!/usr/bin/env python
import sys
import time
import unittest
import logging

import creo
from creo.task_meta import TaskRegisterMemento

# from creo import LocalFile


DELAY = 0.001


class MockLocalFile(creo.LocalFile):

    __metaclass__ = TaskRegisterMemento

    def __init__(self, filename):
        super(MockLocalFile, self).__init__(filename)
        self.timestamp = None

    def exists(self):
        return self.timestamp is not None

    def last_modified(self):
        if not self.exists():
            raise IOError(
                "file '%s' does not exist! Cannot get modified time."
                % self.path)
        return self.timestamp

    def touch(self, timestamp=None):
        self.timestamp = time.time()

if sys.platform == 'darwin':
    logging.info(
        "Changing test delay time for OSX filesystem since it only has 1 "
        "second time resolution")
    DELAY = 1
    # LocalFile = MockLocalFile
LocalFile = creo.LocalFile


class TestTaskBuildFlow(unittest.TestCase):

    def test_build_1(self):

        class TouchTask(creo.Task):
            def run(self):
                for f in self.outputs():
                    f.touch()
                    time.sleep(DELAY)
                return True

        class Step1(TouchTask):
            def outputs(self):
                return [LocalFile("step1.txt")]

        class Step2_1(TouchTask):
            def depends(self):
                return [Step1()]

            def outputs(self):
                return [LocalFile("step2_1.txt")]

        class Step2_2(TouchTask):
            def depends(self):
                return [Step1()]

            def outputs(self):
                return [LocalFile("step2_2.txt")]

        class Step3(TouchTask):
            def depends(self):
                return [Step2_1(), Step2_2()]

            def outputs(self):
                return [LocalFile("step3.txt")]

        class Step4(TouchTask):
            def depends(self):
                return [Step3(), Step2_2()]

            def outputs(self):
                return [LocalFile("step4_1.txt"), LocalFile("step4_2.txt")]

        target_task = Step4()

        runner = creo.TaskManager()
        runner.add(target_task)

        # Run all the tasks
        # logging.info('*'*79)
        # runner.run()

        # Update the first task and ensure other tasks invalidated
        logging.info('*'*79)
        m = LocalFile("mark.txt")
        m.touch()
        time.sleep(DELAY)
        f = LocalFile("step1.txt")
        f.touch()
        time.sleep(DELAY)
        runner.run()
        # Check that the files were updates as expected

        print LocalFile("mark.txt")
        print LocalFile("step1.txt")
        print LocalFile("step2_1.txt")
        print LocalFile("step2_2.txt")
        print LocalFile("step3.txt")
        print LocalFile("step4_1.txt")
        print LocalFile("step4_2.txt")

        self.assertTrue(LocalFile("mark.txt") < LocalFile("step1.txt") < LocalFile("step2_1.txt") < LocalFile("step2_2.txt") < LocalFile("step3.txt") < LocalFile("step4_1.txt") < LocalFile("step4_2.txt"))

        logging.info('*'*79)
        m = LocalFile("mark.txt")
        m.touch()
        time.sleep(DELAY)
        f = LocalFile("step3.txt")
        f.touch()
        time.sleep(DELAY)
        runner.run()
        # Check that the files were updates as expected
        self.assertTrue(LocalFile("step1.txt") < LocalFile("step2_1.txt") < LocalFile("step2_2.txt") < LocalFile("mark.txt") < LocalFile("step3.txt") < LocalFile("step4_1.txt") < LocalFile("step4_2.txt"))

        logging.info('*'*79)
        m = LocalFile("mark.txt")
        m.touch()
        time.sleep(DELAY)
        f = LocalFile("step2_2.txt")
        f.touch()
        time.sleep(DELAY)
        runner.run()
        # Check that the files were updates as expected
        self.assertTrue(LocalFile("step1.txt") < LocalFile("step2_1.txt") < LocalFile("mark.txt") < LocalFile("step2_2.txt") < LocalFile("step3.txt") < LocalFile("step4_1.txt") < LocalFile("step4_2.txt"))
