#!/usr/bin/env python
"""
Module task

:Company: SwissTech Consulting
:Author: Patrick Glass <patrickglass@swisstech.ca>
:Copyright: Copyright 2015 SwissTech Consulting

This software is used for flow development and execution of pipelines
"""
import logging
import weakref
import warnings


# from .memento import MementoMetaclass
from .task_meta import TaskRegisterMemento
from .task_state import PENDING, CHECK, RUNABLE, RUNNING, SUCCESS, FAILED, DISABLED

logger = logging.getLogger(__name__)


class Task(object):

    # Instance caching for same call signature.
    # This allows multiple instation in `requires` which reference the
    # save instance.
    __metaclass__ = TaskRegisterMemento

    # Stores all object instances so they can be iterated over later.
    # we have used a weakref to allow Tasks to be deleted. Must now
    # handle the case when the ref has been gargbage collected.
    instances = weakref.WeakSet()

    # We want to be able to comare base on outputs existsing and
    # timestamp comparison of inputs vs outputs
    use_simple_compare = False

    def __init__(self, *args, **kwargs):

        self.name = self.__class__.__name__
        self.full_name = self.__module__ + '.' + self.name

        self.state = PENDING

        if len(args) > 0:
            raise NotImplementedError(
                "Tasks do not support passing in position arguments yet. You "
                "must only use named arguments!")
        # Each parameter which is passed into this Task is set as an attribute
        for k, v in kwargs.items():
            setattr(self, k, v)

        # Add a weak refence to this instance
        self.instances.add(self)

    def depends(self):
        return []

    def outputs(self):
        raise NotImplementedError()

    def output(self):
        """This method is used to grab the first element of the outputs(). It
        is only meant to be used inside a run method. This class must never be
        implemented.
        """
        if len(self.outputs()) != 1:
            raise RuntimeError(
                "You can only use output() when outputs() returns one file!")
        return self.outputs()[0]

    def run(self):
        raise NotImplementedError()

    def inputs(self):
        """Returns a generator for all list of all direct input references. This
        will not include sub-dependant input references
        """
        for task in self.depends():
            for ref in task.outputs():
                yield ref

    def complete(self):
        """
        Comparison routine to determine if this task is up to date. if `False`
        then this task will need to be run.
        """
        outputs = self.outputs()
        inputs = list(self.inputs())
        # logger.debug("Task: %r outputs: %s", self.name, outputs)
        if len(outputs) == 0:
            warnings.warn(
                "Task %r without outputs has no custom complete() method" % self
            )
            return False
        # If there are no inputs or simple compare is selected we will just
        # ensure that the outputs exists.
        if self.use_simple_compare or len(inputs) == 0:
            return all([ref.exists() for ref in outputs])
        else:
            try:
                # # Ensure that the dependant tasks are completed. Otherwise
                # # we cannot say whether this task is up to date
                # for task in self.depends():
                #     if task.state not in (SUCCESS, DISABLED):
                #         logger.debug("Cannot determine since dependent tasks not complete")
                #         return False

                # logger.debug("Task %r inputs: %s", self, inputs)
                max_in = max([ref.last_modified() for ref in inputs])
                # logger.debug("Task %r inputs last modified: %s", self, max_in)
                min_out = min([ref.last_modified() for ref in outputs])
                # logger.debug("Task %r outputs last modified: %s", self, min_out)
                # Task is complete if all inputs are older than outputs
                is_complete = max_in < min_out
                # if is_complete:
                #     msg = "Task '%s' is up to date!"
                # else:
                #     msg = "Task '%s' is out of date and needs to be run!"
                # logger.debug(msg, self.name)
                return is_complete
            except (IOError, KeyError):
                # logger.debug("Task '%s' is out of date and needs to be run!", self.name)
                # One of the files did not exist. We definately have to run.
                # or the Config entry did not exist and so we also have to run.
                return False

    @classmethod
    def get_instances(cls):
        """This method is used to get all of the Task instances

        we have used a weakref to allow Tasks to be deleted. Must now
        handle the case when the ref has been gargbage collected.
        """
        warnings.warn("This method is deprecated. Please use Task.instances",
                      DeprecationWarning)
        return cls.instances

    def __repr__(self):
        return "%s(%r)" % (self.name, self.__dict__)

    def __str__(self):
        """Print out the Task object in a pretty format"""
        s = "Task: '%s'" % self.name
        is_complete = self.complete()
        if not is_complete:
            s += " needs to be run!\n"
            s += '  Inputs:\n'
            for i in self.inputs():
                s += "    %s\n" % i.to_string(True)
            s += '  Outputs:\n'
            for i in self.outputs():
                s += "    %s\n" % i.to_string(True)
        else:
            s += " is up to date!\n"
        return s
