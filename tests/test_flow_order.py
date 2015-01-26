#!/usr/bin/env python
import gc
import unittest
from creo import Task
from creo.dependancy import FileSetDep as File, ConfigDep as Config

def touch_or_create(filename):
    if os.path.exists(filename):
        os.utime(filename, None)
    else:
        file(filename, 'w')

class TestTaskBuildFlow(unittest.TestCase):

    def test_build_1(self):
        @Task(inputs=None, outputs=File("step1.txt"))
        def step1():
            touch_or_create("step1.txt")

        @Task(inputs=File("step1.txt"), outputs=File("step2_1.txt"))
        def step2_1():
            touch_or_create("step2_1.txt")

        @Task(inputs=step1, outputs=File("step2_2.txt"))
        def step2_2():
            touch_or_create("step2_2.txt")

        @Task(inputs=[step2_2, step2_1], outputs=File("step3.txt"))
        def step3():
            touch_or_create("step3.txt")

        @Task(inputs=[File("step3.txt"), File("step2_2.txt")], outputs=[File("step4_1.txt"), File("step4_2.txt")])
        def step4():
            touch_or_create("step4_1.txt")
            touch_or_create("step4_2.txt")

        # Print the tasks
        for t in Task.getinstances():
            print "Task: ", t.name, t.status

        # Run all the tasks
        Task.run()

        self.assertTrue(False)
