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

from .memento import MementoMetaclass


logger = logging.getLogger(__name__)


class Task(object):

    # Instance caching for same call signature.
    # This allows multiple instation in `requires` which reference the
    # save instance.
    __metaclass__ = MementoMetaclass

    # Stores all object instances so they can be iterated over later.
    # we have used a weakref to allow Tasks to be deleted. Must now
    # handle the case when the ref has been gargbage collected.
    instances = weakref.WeakSet()

    # We want to be able to comare base on outputs existsing and
    # timestamp comparison of inputs vs outputs
    use_simple_compare = False

    def __init__(self, *args, **kwargs):

        # logger.debug("Task: %s.__init__(%s, %s)",
        #              self.__class__.__name__, args, kwargs)

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

    def run(self):
        raise NotImplementedError()

    def inputs(self):
        """Returns a generator for all list of all direct input targets. This
        will not include sub-dependant input targets
        """
        for task in self.depends():
            for target in task.outputs():
                yield target

    def complete(self):
        """
        If the task has any outputs, return ``True`` if all outputs exists.
        Otherwise, return ``False``.

        However, you may freely override this method with custom logic.
        """
        outputs = self.outputs()
        inputs = list(self.inputs())
        # logger.debug("Task: %r outputs: %s", self.__class__.__name__, outputs)
        if len(outputs) == 0:
            warnings.warn(
                "Task %r without outputs has no custom complete() method" % self
            )
            return False
        # If there are no inputs or simple compare is selected we will just
        # ensure that the outputs exists.
        if self.use_simple_compare or len(inputs) == 0:
            return all([target.exists() for target in outputs])
        else:
            try:
                logger.debug("Task %r inputs: %s", self, inputs)
                max_in = max([target.last_modified() for target in inputs])
                logger.debug("Task %r inputs last modified: %s", self, max_in)
                min_out = min([target.last_modified() for target in outputs])
                logger.debug("Task %r outputs last modified: %s", self, min_out)
                # Task is complete if all inputs are older than outputs
                is_complete = max_in < min_out
                if is_complete:
                    msg = "Task %r is up to date!"
                else:
                    msg = "Task %r is out of date and needs to be run!"
                logger.debug(msg, self)
                return is_complete
            except (IOError, KeyError):
                logger.debug("Task %r is out of date and needs to be run!", self)
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
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)

    # def __str__(self):
    #     """Print out the Task object in a pretty format"""
    #     return "Task: {__class__}".format(*self.__dict__)
