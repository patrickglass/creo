#!/usr/bin/env python
"""
Module pmcx

:Company: SwissTech Consulting
:Author: Patrick Glass <patrickglass@swisstech.ca>
:Copyright: Copyright 2014 SwissTech Consulting

This software is used for flow development and execution for the
IC Physical Design group.
"""
import os
import logging
import functools
import weakref
import graph

from dependancy import Dependancy, FileSetDep


class STATE(object):
    ALWAYS, DEPEND, RUNNABLE, SUCCESS, FAILURE = range(5)

class Task(object):
    """
    Task represents a named node and function to representing the task.
    The task can have dependancies and others can depend on the tasks output.
    """
    _instances = weakref.WeakSet()

    def __init__(self, inputs=None, outputs=None,
                 pre_target=None, post_target=None,
                 *args):

        self.name = None
        self.description = None

        self.inputs = set()
        self.outputs = set()

        # If there are no updates this task is immediately runnable
        if inputs is None:
            self.state = STATE.RUNNABLE
        else:
            self.state = STATE.DEPEND
            if isinstance(inputs, (list, tuple)):
                for i in inputs:
                    self.set_inputs(i)
            else:
                self.set_inputs(inputs)

        # Set the output dependancys based on the input args
        # if there are not output this target will always be run
        if outputs is None:
            self.state = STATE.ALWAYS
        else:
            if isinstance(outputs, (list, tuple)):
                for o in outputs:
                    self.set_outputs(o)
            else:
                self.set_outputs(outputs)

        self.pre_target = None
        self.target = None
        self.post_target = None
        print("TASK INIT")
        # Add a weak refence to this instance
        self._instances.add(self)

    def __call__(self, func):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        if func.__name__ in [t.name for t in Task.getinstances()]:
            raise RuntimeError("@Task function %s must be unique" % func.__name__)
        self.name = func.__name__
        self.description = func.__doc__ or ""

        self.target = func
        functools.update_wrapper(self, func)
        print("TASK CALL %s" % self.name)
        return self

    def __str__(self):
        """Print out the Task object in a pretty format"""
        return "TASK: %s %s" % (self.name, self.state)

    def set_inputs(self, obj):
        """Handles the inputs and create dependancies from them

        Allowed inputs are function which must have been run successfully
        Files if the input is a string
        Or a list of either of the above
        """
        if isinstance(obj, Dependancy):
            # ideal input arg is an actual dependancy object.
            self.inputs.add(obj)
        elif not isinstance(obj, basestring):
            # if the input is of type string assume it is a file
            self.inputs.add(FileSetDep(obj))
        elif hasattr(obj, '__call__'):
            # The function must be another task
            # If so add all of its output as inputs on this task
            if isinstance(obj, Task):
                for i in obj.outputs:
                    self.inputs.add(i)
            else:
                raise RuntimeError("input dependancy function must be references to another @Task decorated function!" + str(obj))
        else:
            raise TypeError("Input Dependancy is of the incorrect type!")

    def set_outputs(self, obj):
        # if the input is a string assume it is a file
        if isinstance(obj, Dependancy):
            self.inputs.add(obj)
        elif not isinstance(obj, basestring):
            self.inputs.add(FileSetDep(obj))
        else:
            raise TypeError("Input Dependancy is of the incorrect type!")

    def check_rebuild(self):
        """Checks the inputs vs the outputs to determine if this target
        is required to be rebuilt.
        Returns True if rebuild is required
        returns False if target is up to date
        """
        for i in self.inputs:
            for o in self.outputs:
                if i >= o:
                    # if the input is newer than the output rebuild.
                    return True
        return False

    def check_dependancies(self):
        # Check that the dependancies are all up to date
        for dep in self.inputs:
            if self.state != STATE.SUCCESS:
                logging.info("Task ran Successfully!")
            elif self.state == STATE.RUNNABLE:
                logging.info("Task can be run. All Deps up to date!")
            elif self.state == STATE.RUNNABLE:
                logging.info("Task can be run. All Deps up to date!")
        return True

    def run(self):
        # Run the precondition
        if self.pre_target is not None:
            self.pre_target()
        # Run the main target
        self.target()
        # Run the post condition
        if self.post_target is not None:
            self.post_target()


    @classmethod
    def getinstances(cls):
        """This method is used to get all of the Task instances

        we have used a weakref to allow Tasks to be deleted. Must now
        handle the case when the ref has been gargbage collected.
        """
        return cls._instances

    @classmethod
    def run(cls, target=None):
        print("Starting Build...")
        print("Found %s targets!" % len(Task.getinstances()))
        for task in Task.getinstances():
            print(task)
            # State machine for each build task
            if task.state is STATE.DEPEND:
                rebuild = task.check_rebuild()
                if rebuild:
                    # if the task has all
                    task.state = STATE.RUNNABLE
            elif task.state is STATE.ALWAYS or task.state == STATE.RUNNABLE:
                try:
                    task.run()
                    task.state = STATE.SUCCESS
                except Exception as e:
                    logging.error("Task Exception: %s" % e)
                    task.state = STATE.FAILURE
            else:
                task.state = STATE.DEPEND
