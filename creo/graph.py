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
        self.inputs = {}
        self.outputs = {}

    def __str__(self):
        return self.name

    def print_edges(self):
        print "%s:\tINPUTS: %s" % (self.name, map(str, self.inputs.keys()))
        print "%s:\tOUTPUTS: %s" % (self.name, map(str, self.outputs.keys()))


class Graph:
    def __init__(self):
        self.nodes = {}

    def add(self, name, input=None, inputs=None, output=None, outputs=None):
        # node = Node(name)
        node, created = self.get_or_create(name)

        # Create edges if specified, either by name or obj.
        if input:
            self.add_edge(input, name)

        if output:
            self.add_edge(name, output)

        if inputs:
            for o in inputs:
                self.add_edge(o, name)

        if outputs:
            for o in outputs:
                self.add_edge(name, o)

        self.nodes[name] = node
        # print node.inputs
        # print node.outputs
        return node

    def add_edge(self, start_node, end_node):
        start, created = self.get_or_create(start_node)
        end, created = self.get_or_create(end_node)
        start.outputs[end.name] = end
        end.inputs[start.name] = start


    def get(self, name):
        return self.nodes[name]
        # if name in self.nodes:
        #     return self.nodes[name]
        # else:
        #     return None

    def get_or_create(self, name):
        if name in self.nodes:
            return (self.nodes[name], True)
        else:
            # node = self.add(name)
            node = Node(name)
            self.nodes[name] = node
            return (node, True)

    def list(self):
        """returns an toplogical sorted list of elements"""
        return self.nodes

