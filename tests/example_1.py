#!/usr/bin/env python
import sys
import time
import logging

import creo
from creo import LocalFile


logging.basicConfig(level=logging.DEBUG)

DELAY = 0.001
if sys.platform == 'darwin':
    logging.info(
        "Changing test delay time for OSX filesystem since it only has 1 "
        "second time resolution")
    DELAY = 2


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
LocalFile("mark.txt").touch()
time.sleep(DELAY)
LocalFile("step1.txt").touch()
time.sleep(DELAY)
runner.run()

print LocalFile("mark.txt").to_string(True)
print LocalFile("step1.txt").to_string(True)
print LocalFile("step2_1.txt").to_string(True)
print LocalFile("step2_2.txt").to_string(True)
print LocalFile("step3.txt").to_string(True)
print LocalFile("step4_1.txt").to_string(True)
print LocalFile("step4_2.txt").to_string(True)

# Check that the files were updates as expected
assert(LocalFile("mark.txt") < LocalFile("step1.txt") < LocalFile("step2_1.txt") < LocalFile("step2_2.txt") < LocalFile("step3.txt") < LocalFile("step4_1.txt") < LocalFile("step4_2.txt"))

logging.info('*'*79)
LocalFile("mark.txt").touch()
time.sleep(DELAY)
LocalFile("step3.txt").touch()
time.sleep(DELAY)
runner.run()

print LocalFile("mark.txt").to_string(True)
print LocalFile("step1.txt").to_string(True)
print LocalFile("step2_1.txt").to_string(True)
print LocalFile("step2_2.txt").to_string(True)
print LocalFile("step3.txt").to_string(True)
print LocalFile("step4_1.txt").to_string(True)
print LocalFile("step4_2.txt").to_string(True)

# Check that the files were updates as expected
assert(LocalFile("step1.txt") < LocalFile("step2_1.txt") < LocalFile("step2_2.txt") < LocalFile("mark.txt") < LocalFile("step3.txt") < LocalFile("step4_1.txt") < LocalFile("step4_2.txt"))

logging.info('*'*79)
LocalFile("mark.txt").touch()
time.sleep(DELAY)
LocalFile("step2_2.txt").touch()
time.sleep(DELAY)
runner.run()

print LocalFile("mark.txt")
print LocalFile("step1.txt")
print LocalFile("step2_1.txt")
print LocalFile("step2_2.txt")
print LocalFile("step3.txt")
print LocalFile("step4_1.txt")
print LocalFile("step4_2.txt")

# Check that the files were updates as expected
assert(LocalFile("step1.txt") < LocalFile("step2_1.txt") < LocalFile("mark.txt") < LocalFile("step2_2.txt") < LocalFile("step3.txt") < LocalFile("step4_1.txt") < LocalFile("step4_2.txt"))

logging.info('*'*79)
logging.info('*'*79)
runner.status()

logging.info('*'*79)
logging.info('*'*79)
LocalFile("mark.txt").touch()
time.sleep(DELAY)
LocalFile("step2_2.txt").touch()
time.sleep(DELAY)
runner.status()
