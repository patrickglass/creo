#!/usr/bin/env python
"""
Module task

:Company: SwissTech Consulting
:Author: Patrick Glass <patrickglass@swisstech.ca>
:Copyright: Copyright 2015 SwissTech Consulting

This software is used for flow development and execution of pipelines
"""
import logging
import warnings
import threading
import multiprocessing
import types


from task import Task
from .task_state import PENDING, CHECK, RUNABLE, RUNNING, SUCCESS, FAILED, DISABLED
from .messages import Message, red, green, blue, yellow, magenta, cyan


# logger = logging.getLogger(__name__)
logger = Message(__name__)


class Worker(object):

    def __init__(self, group=None, target=None, name=None, *args, **kwargs):
        self.group = group
        self.target = target
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def run(self):
        return self.target(*self.args, **self.kwargs)

    def join(self):
        pass


class ProcessWorker(multiprocessing.Process):
    pass


class ThreadWorker(threading.Thread):
    pass


class TaskManager(object):

    def __init__(self, task_base=Task, worker_type=Worker):
        self.base_class = task_base
        self.worker_type = worker_type
        self.worker_results = {}

    def _target_to_instance(self, target):
        # We allow class names to be specified as a string
        # Find the actual class from the string
        if isinstance(target, basestring):
            target = self.base_class.class_by_name(target)

        # Check whether the value is a class or instance
        # we want to return only instances
        if isinstance(target, (type, types.ClassType)):
            return target()
        else:
            return target

    def _get_tasks(self, target):
        """
        if target is passed in get only related tasks
        otherwise get all defined task instances
        """
        if target:
            return TaskManager.all_deps(self._target_to_instance(target))
        else:
            warnings.warn(
                "You must specify the target. Discovery is not supported yet",
                DeprecationWarning
            )
            # Get all defined classes and instantiate them.
            # Then grab and return all instances.
            for task_cls in self.base_class.classes.values():
                task_cls()

            return self.base_class.instances.values()
            # return self.base_class.classes.values()

    # def add(self, target):
    #     logger.debug("Adding target %s to pool." % target)
    #     warnings.warn(
    #         "'add' is deprecated. All calls should change to passing target to status, run, clean, and force!",
    #         DeprecationWarning
    #     )
    #     self.targets.append(target)

    def status(self, target=None):
        tasks = self._get_tasks(target)
        for task in tasks:
            try:
                s = "Task: " + green("'%s'" % task.name)
                is_complete = task.complete()
                if not is_complete:
                    s += " needs to be run!\n"
                    s += yellow('  Inputs:\n')
                    for i in task.inputs():
                        s += cyan("    %s\n" % i.to_string(True))
                    s += yellow('  Outputs:\n')
                    for i in task.outputs():
                        s += cyan("    %s\n" % i.to_string(True))
                else:
                    s += " is up to date!"
                logger.info(s)
            except NotImplementedError:
                logger.info("%s is not implemented correctly. Skipping..." % task.name)

    def clean(self, target=None, level=0):
        """Clean iterates through all outputs and will call remove() on it if
        the level of the file is lower than specified. This allows you to
        have different levels of clean.
        """
        tasks = self._get_tasks(target)
        # go through each task and check the outputs
        for task in tasks:
            for output in task.outputs():
                if output.level <= level:
                    logging.info("Removing: %s", output)
                else:
                    logging.debug("Preserving: %s", output)

    def force(self, target=None):
        """Will force all outputs of specified target to be up to date. This
        will have the same effect as `touch`ing the output files.
        """
        task = self._target_to_instance(target)
        logging.info("Forcing '%s' to be updated!", task)
        for output in task.outputs():
            logging.debug("Force Update: %s", output)

    def run_new_state(self):
        for target in self.targets:
            for task in TaskManager.all_deps(target):
                self.update_state(task)

    def update_state(self, task):
        if task.state == PENDING:
            if len(task.inputs()) == 0:
                task.state = CHECK
            elif all([t.state for t in task.inputs() if t.state != SUCCESS]):
                task.state = CHECK

            if task.state == CHECK:
                if task.complete():
                    task.state == SUCCESS
                else:
                    task.state == RUNABLE
        elif task.state == RUNNING:
            # Check with the results dict if this task has results posted
            if task.name in self.worker_results:
                result = self.worker_results[task.name]
                is_complete = task.complete()
                if not result:
                    logging.warn(
                        "%s failed with return code: %s",
                        task.name, result)
                    task.state == FAILED
                elif not is_complete():
                    task.state == FAILED
                    logging.error(
                        RuntimeError,
                        "%s failed complete() task check. This should "
                        "never occur since the task should be able to "
                        "determine success without relying on job return "
                        "code. Please report this error!",
                        task.name)
                    # raise RuntimeError()
                else:
                    logging.debug(
                        "%s completed successfully!", task.name)
                    task.state == SUCCESS
            # Final states are SUCCESS, FAILED, DISABLED. Do Nothing
            # for state RUNABLE external process will queue the run and
            # change it status once completed.

    @staticmethod
    def all_deps(task):
        # logger.debug("Flatten Task: %s", task)
        for dependent in task.depends():
            # logger.debug("Flatten SubTask: %s", dependent)
            for subtask in TaskManager.all_deps(dependent):
                yield subtask
        # logger.debug("Yield Main incomplete Task: %s", task)
        yield task

    @staticmethod
    def flatten_incomplete_tasks(task):
        # logger.debug("Flatten Task: %s", task)
        for dependent in task.depends():
            # logger.debug("Flatten SubTask: %s", dependent)
            for subtask in TaskManager.flatten_incomplete_tasks(dependent):
                yield subtask
        if not task.state == DISABLED and not task.complete():
            # logger.debug("Yield Main incomplete Task: %s", task)
            yield task

    def run(self, target=None):
        target = self._target_to_instance(target)

        for task in TaskManager.flatten_incomplete_tasks(target):
            logger.info("Running Task: %s", task.name)
            worker = self.worker_type(target=task.run, name=task.name)
            worker.join()
            ret_code = worker.run()
            if ret_code and task.complete():
                logger.info("\t\t'%s' Completed", task.name)
                task.state = SUCCESS
            else:
                logger.error("*** '%s' FAILED", task.name)
                print(task)
                task.state = FAILED
                raise RuntimeError(
                    "Task '%s' failed to run or had bad exit code. "
                    "Exiting run...", task)
