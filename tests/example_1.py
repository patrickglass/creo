#!/usr/bin/env python
import time
import logging

import creo
from creo import LocalFile


logging.basicConfig(level=logging.DEBUG)


class TouchTask(creo.Task):
    def run(self):
        for f in self.outputs():
            f.touch()
            time.sleep(0.1)
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

# Run all the tasks
logging.info('*'*79)
runner.run(target_task)

# Update the first task and ensure other tasks invalidated
logging.info('*'*79)
LocalFile("mark.txt").touch()
time.sleep(0.1)
LocalFile("step1.txt").touch()
runner.run(target_task)
# Check that the files were updates as expected
assert(LocalFile("mark.txt") < LocalFile("step1.txt") < LocalFile("step2_1.txt") < LocalFile("step2_2.txt") < LocalFile("step3.txt") < LocalFile("step4_1.txt") < LocalFile("step4_2.txt"))

logging.info('*'*79)
LocalFile("mark.txt").touch()
time.sleep(0.1)
LocalFile("step3.txt").touch()
runner.run(target_task)
# Check that the files were updates as expected
assert(LocalFile("step1.txt") < LocalFile("step2_1.txt") < LocalFile("step2_2.txt") < LocalFile("mark.txt") < LocalFile("step3.txt") < LocalFile("step4_1.txt") < LocalFile("step4_2.txt"))

logging.info('*'*79)
LocalFile("mark.txt").touch()
time.sleep(0.1)
LocalFile("step2_2.txt").touch()
runner.run(target_task)
# Check that the files were updates as expected
assert(LocalFile("step1.txt") < LocalFile("step2_1.txt") < LocalFile("mark.txt") < LocalFile("step2_2.txt") < LocalFile("step3.txt") < LocalFile("step4_1.txt") < LocalFile("step4_2.txt"))
