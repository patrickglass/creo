#!/usr/bin/env python
"""
Module reference

:Company: SwissTech Consulting
:Author: Patrick Glass <patrickglass@swisstech.ca>
:Copyright: Copyright 2015 SwissTech Consulting

This software is used for flow development and execution of pipelines
"""
import os
import logging
import functools
import datetime

from .packages import creoconfig


logger = logging.getLogger(__name__)


@functools.total_ordering
class Reference(object):

    def __init__(self, level=0):
        self.level = level

    def exists(self):
        raise NotImplementedError()

    def remove(self):
        raise NotImplementedError(
            "Remove is called by TaskManager.clean() and is used to cleanup "
            "the working directory. Each `Reference` can declare its own "
            "level which allows fine grain control of what to remove.")

    def last_modified(self):
        msg = """You cannot use %s class in Tasks which compare by
        last_modified timestamps.""" % self.__class__
        logger.error(msg)
        raise NotImplementedError(msg)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        "Check whether the two instancse have the same modified time"
        return (self.last_modified() == other.last_modified())

    def __ne__(self, other):
        "Check whether the two instancse have different modified times"
        return (self.last_modified() != other.last_modified())

    def __lt__(self, other):
        "Check whether this instance was last modified before the other"
        return (self.last_modified() < other.last_modified())


class LocalDirectory(Reference):

    def __init__(self, path, create=False, level=0):
        super(LocalDirectory, self).__init__(level)
        self.file = path
        self.directory = os.path.realpath(path)
        if create:
            self.mkdir()

    def mkdir(self):
        if not os.path.exists(self.directory):
            logger.debug(
                "Making dir '%s' for file '%s'", self.directory, self.file)
            os.makedirs(self.directory)

    def exists(self):
        return os.path.exists(self.file)

    def last_modified(self):
        if self.exists():
            last_mod = os.stat(self.file).st_mtime
            # logger.debug("%s was modified %f.", self.file, last_mod)
            return last_mod
        raise IOError("file '%s' does not exist! Cannot get modified time."
                      % self.file)

    def to_string(self, compact=True):
        try:
            ts = datetime.datetime.fromtimestamp(self.last_modified())
            time_str = ts.strftime('%Y-%m-%d %H:%M:%S.%f')
        except IOError:
            time_str = "<-- MISSING"
        if compact:
            fmt = "%s: %-35s\t%s"
        else:
            fmt = "%s: %s\n\tModified: %s"
        return fmt % (self.__class__.__name__, self.file, time_str)

    def __str__(self):
        return self.file


class LocalFile(LocalDirectory):

    def __init__(self, filename, create=True, level=0):
        super(LocalFile, self).__init__(level)
        self.file = filename
        self.directory = os.path.dirname(os.path.realpath(filename))
        if create:
            self.mkdir()

    def last_modified(self):
        if self.exists():
            last_mod = os.path.getmtime(self.file)
            # logger.debug("%s was modified %f.", self.file, last_mod)
            return last_mod
        raise IOError("file '%s' does not exist! Cannot get modified time."
                      % self.file)

    def touch(self, timestamp=None):
        with open(self.file, 'a'):
            os.utime(self.file, timestamp)

    def open(self, mode='w'):
        return open(self.file, mode)


SETTINGS_FILE = 'creo_build.xml'
env = creoconfig.Config(SETTINGS_FILE)


class ConfigEntry(Reference):

    def __init__(self, key, config=env, level=0):
        super(ConfigEntry, self).__init__(level)
        self.config = config
        self.key = key

    def set(self, value):
        return self.config.set(self.key, value)

    def get(self, default=None):
        return self.config.get(self.key, default)

    def last_modified(self):
        last_mod = self.config.last_modified(self.key)
        logger.debug("Config '%s' was modified %f.", self.key, last_mod)
        return last_mod

    def exists(self):
        return self.config.get(self.key) is not None
