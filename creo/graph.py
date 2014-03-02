#!/usr/bin/env python
"""
Module graph

Implements a directed acyclic graph (DAG) which will throw an error
when a circular dependancy is created. A topological sort is used to determine
what nodes can be run first.
"""

class Node:
    def __init__(self, name):
       self.name = name
       self.inputs = []
       self.outputs = []

    def add_input(self, name):
        self.inputs.append(name)

    def add_output(self, name):
        self.outputs.append(name)


class Graph:
    def __init__(self):
        self.nodes = {}

    def add(self, name, before=None, after=None):
        node = Node(name)
        self.nodes[name] = node
