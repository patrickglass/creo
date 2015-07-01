#!/usr/bin/env python
"""
Module task

:Company: SwissTech Consulting
:Author: Patrick Glass <patrickglass@swisstech.ca>
:Copyright: Copyright 2015 SwissTech Consulting

This software is used for flow development and execution of pipelines
"""
import logging


logger = logging.getLogger(__name__)


class TaskManager(object):

    def __init__(self):
        # if not isinstance(task_class, Task):
        #     raise TypeError('task_class must be of type creo.Task!')
        # self.tasks = task_class.instances
        pass

    def status(self, target=None):
        # for task in self.tasks:
        #     logger.info(task)
        for task in TaskManager.flatten_incomplete_tasks(target):
            logger.info("\tTask: %s", task)

    @staticmethod
    def flatten_incomplete_tasks(task):
        # logger.debug("Flatten Task: %s", task)
        for dependant in task.depends():
            # logger.debug("Flatten SubTask: %s", dependant)
            for subtask in TaskManager.flatten_incomplete_tasks(dependant):
                yield subtask
        if not task.complete():
            # logger.debug("Yield Main incomplete Task: %s", task)
            yield task

    def run(self, target=None):
        for task in TaskManager.flatten_incomplete_tasks(target):
            logger.info("Running Task: %s", task)
            ret_code = task.run()
            if ret_code:
                logger.info("Task %s Completed", task)
            else:
                logger.error("*** Task %s FAILED", task)
