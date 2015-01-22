#!/usr/bin/env python
"""
Module pmcx

:Company: SwissTech Consulting
:Author: Patrick Glass <patrickglass@swisstech.ca>
:Copyright: Copyright 2014 SwissTech Consulting

This software is used for flow development and execution for the
IC Physical Design group.
"""
import functools

import graph


def NOP_FUNCTION():
    pass

def SUCCESS_FUNCTION():
    return True

class BuildFlow(graph.Graph):
    def __init__(self):
        super(BuildFlow, self).__init__()


class Task(graph.Node):
    """
    Task represents a named node and function to representing the task.
    The task can have dependancies and others can depend on the tasks output.
    """
    def __init__(self, name):
        self.task_checks = [SUCCESS_FUNCTION,]
        self.task_pre = [NOP_FUNCTION,]
        self.task_function = [NOP_FUNCTION,]
        self.task_post = [NOP_FUNCTION,]

        assert(name)

        super(Task, self).__init__(name)



def follows1(func_name):
    """
    """
    def wrapper(f):
        print "Inside wrapper()"
        def wrapped_f(*args, **kwargs):
            print "Inside wrapped_f()"
            print "Decorator arguments:", func_name
            f(*args, **kwargs)
            print "After f(*args, **kwargs)"
        return wrapped_f
    return wrapper


class follows(object):

    def __init__(self, function_name):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        print "Inside __init__()"
        self.arg1 = function_name

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        print "Inside __call__()"
        def wrapped_f(*args):
            print "Inside wrapped_f()"
            print "Decorator arguments:", self.arg1
            f(*args)
            print "After f(*args)"
        functools.update_wrapper(self, f)
        return wrapped_f


class decoratorWithoutArguments(object):

    def __init__(self, f):
        """
        If there are no decorator arguments, the function
        to be decorated is passed to the constructor.
        """
        print "Inside __init__()"
        self.f = f
        functools.update_wrapper(self, f)

    def __call__(self, *args):
        """
        The __call__ method is not called until the
        decorated function is called.
        """
        print "Inside __call__()"
        self.f(*args)
        print "After self.f(*args)"
