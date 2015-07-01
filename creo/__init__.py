"""
:Company: SwissTech Consulting
:Author: Patrick Glass <patrickglass@swisstech.ca>
:Copyright: Copyright 2015 SwissTech Consulting
"""
import os
import sys
import inspect
import subprocess


# use this if you want to include modules from a subfolder
folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
pkg_folder = os.path.realpath(os.path.abspath(os.path.join(folder, "packages")))
if pkg_folder not in sys.path:
    sys.path.insert(0, pkg_folder)


from .task import Task
from .task_manager import TaskManager
from .reference import Reference, LocalFile, LocalDirectory, ConfigEntry, env


def process_cmd(command):
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    text = p.stdout.read()
    retcode = p.wait()
    return retcode, text
