#!/usr/bin/env python
"""
Module fileset

:Company: SwissTech Consulting
:Author: Patrick Glass <patrickglass@swisstech.ca>
:Copyright: Copyright 2015 SwissTech Consulting

This class is used to create a handle to a group of files and enable
extracting and comparing timestamps.
"""
import glob
import os
import time


class Dependancy(object):
    """
    Dependancy class

    This class is used to create a handle to a group of files and enable
    extracting and comparing timestamps.
    """
    def __init__(self, *args):
        self.args = args
        self.t_max = self.t_min = None

    def _get_time_stamp(self):
        """for the given files find the max and min time window"""
        raise NotImplemented("This method needs to be defined in subclass")

    def _update_and_check_args(self, other):
        if not isinstance(self, Dependancy) or not isinstance(other, Dependancy):
            raise AttributeError('Can only compare Dependancy class objects')
        if not self.t_max or not self.t_min:
            self._get_time_stamp()
        if not other.t_max or not other.t_min:
            other._get_time_stamp()

    def __str__(self):
        if not self.t_max or not self.t_min:
            self._get_time_stamp()
        data = (
            time.strftime("%b %d %Y %H:%M:%S", time.localtime(self.t_min)),
            time.strftime("%b %d %Y %H:%M:%S", time.localtime(self.t_max)),
            '\n\t'.join(self.paths),
        )
        return "Dependancy: from [%s] to [%s]:\n\t%s" % data

    def __lt__(self, other):
        """
        returns `True` if the left object is older than the right object when
        using the less than `<` operator
        """
        self._update_and_check_args(other)
        return self.t_max < other.t_min

    def __gt__(self, other):
        """
        returns `True` if the left object is newer than the right object when
        using the greater than `>` operator
        """
        self._update_and_check_args(other)
        return self.t_min > other.t_max

    def __eq__(self, other):
        self._update_and_check_args(other)
        return self.t_max == other.t_max and self.t_min == other.t_min

    def __ne__(self, other):
        return not (self == other)

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other


class FileSetDep(Dependancy):
    """
    FileSet class

    This class is used to create a handle to a group of files and enable
    extracting and comparing timestamps.
    """
    def __init__(self, *args):
        self.paths = []
        self.args = args
        if not args:
            raise ValueError("FileSet must be passed in files glob patterns")

        self.t_max = self.t_min = None

    def _get_time_stamp(self):
        """for the given files find the max and min time window"""
        for arg in self.args:
            if isinstance(arg, basestring):
                self.paths.extend(glob.glob(arg))
            else:
                raise ValueError("Argument must be string pathnames! %s" % arg)

        if not self.paths:
            self.t_max = self.t_min = None
            return None
            # raise ValueError("Glob pattern did not match any files %s" % str(self.args))

        for path in self.paths:
            try:
                t = os.path.getmtime(path)
                if self.t_min is None or self.t_max is None:
                    self.t_max = self.t_min = t
                if t > self.t_max:
                    self.t_max = t
                elif t < self.t_min:
                    self.t_min = t
            except os.error:
                raise ValueError("File could not be accessed: '%s'" % str(path))
        return self.t_min, self.t_max
