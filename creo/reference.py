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

from .packages import creoconfig


logger = logging.getLogger(__name__)


@functools.total_ordering
class Reference(object):

    def exists(self):
        raise NotImplementedError()

    def last_modified(self):
        msg = """You cannot use %s classes in Tasks which compare by
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

    def __init__(self, path):
        self.path = path

    def exists(self):
        return os.path.exists(self.path)

    def last_modified(self):
        if self.exists():
            last_mod = os.stat(self.path).st_mtime
            logger.debug("%s was modified %f.", self.path, last_mod)
            return last_mod
        logger.error("Cannot get timestamp for missing file %s", self.path)
        raise IOError("file '%s' does not exist! Cannot get modified time."
                      % self.path)


class LocalFile(LocalDirectory):

    def __init__(self, filename):
        self.path = filename

    def last_modified(self):
        if self.exists():
            last_mod = os.path.getmtime(self.path)
            logger.debug("%s was modified %f.", self.path, last_mod)
            return last_mod
        logger.error("Cannot get timestamp for missing file %s", self.path)
        raise IOError("file '%s' does not exist! Cannot get modified time."
                      % self.path)

    def touch(self):
        if self.exists():
            os.utime(self.path, None)
        else:
            file(self.path, 'w')


SETTINGS_FILE = 'creo_build.xml'
env = creoconfig.Config(SETTINGS_FILE)


class ConfigEntry(Reference):

    def __init__(self, key, config=env):
        self.config = config
        self.key = key

    def set(self, key, value):
        return self.config.set(key, value)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def last_modified(self, key):
        last_mod = self.config.last_modified(key)
        logger.debug("Config '%s' was modified %f.", key, last_mod)
        return last_mod

    def exists(self):
        return self.config.get(self.key) is not None
