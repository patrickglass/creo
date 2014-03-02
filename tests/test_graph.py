#!/usr/bin/env python

import unittest
from creo.graph import Graph, Node

class TestNodes(unittest.TestCase):

    def test_node_init_name(self):
        self.assertEqual(Node('testname').name, 'testname')

    def test_node_add_input_by_name(self):
        n1 = Node('testname')
        n2 = Node('testname2')
        n2.add_input('testname')
        self.assertEqual(len(n2.inputs), 1)
        self.assertEqual(n2.inputs[0], 'testname')

    def test_node_add_input_by_instance(self):
        n1 = Node('testname')
        n2 = Node('testname2')
        n2.add_input(n1)
        self.assertEqual(len(n2.inputs), 1)
        self.assertEqual(n2.inputs[0], 'testname')


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g = Graph()

    def test_graph_create_node(self):
        self.g.add('firstnode')
        self.assertEqual(len(self.g.nodes), 1)

    def test_graph_create_node2(self):
        self.g.add('firstnode')
        self.g.add('secondnode')
        self.assertEqual(len(self.g.nodes), 2)

    def test_graph_recreate_node(self):
        self.g.add('firstnode')
        self.g.add('secondnode')
        self.g.add('firstnode')
        self.g.add('firstnode')
        self.assertEqual(len(self.g.nodes), 2)