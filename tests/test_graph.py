#!/usr/bin/env python

import unittest
from creo.graph import Graph, Node

class TestNodes(unittest.TestCase):

    def test_node_init_name(self):
        self.assertEqual(Node('testname').name, 'testname')

    # def test_node_add_input_by_name(self):
    #     n1 = Node('testname')
    #     n2 = Node('testname2')
    #     n2.inputs(n1)
    #     self.assertEqual(len(n2.inputs), 1)
    #     self.assertEqual(n2.inputs[0], n1)

    # def test_node_add_input_by_instance(self):
    #     n1 = Node('testname')
    #     n2 = Node('testname2')
    #     n2.inputs.append(n1)
    #     self.assertEqual(len(n2.inputs), 1)
    #     self.assertEqual(n2.inputs[0], n1)


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g = Graph()

    def test_graph_create_node(self):
        self.g.add('testname')
        self.assertEqual(self.g.get('testname').name, 'testname')

    def test_graph_get_node(self):
        self.g.add('firstnode')
        node = self.g.get('firstnode')
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


class TestGraphScenario1(unittest.TestCase):
    def setUp(self):
        self.g = Graph()
        self.g.add('0')
        self.g.add('1', input='0')
        self.g.add('2', input='0')
        self.g.add('4', inputs=['3', '1'])
        self.g.add('5', input='1', output='6')
        self.g.add('6')
        self.g.add('3', input='2')
        self.g.add('7', inputs=['4', '6'])
        self.g.add('8', input='3', output='4')
        print "setup complete."

    def test_node_0(self):
        n = self.g.get('0')
        self.assertEquals(len(n.inputs), 0)
        self.assertEquals(len(n.outputs), 2)

    def test_node_1(self):
        n = self.g.get('1')
        self.assertEquals(len(n.inputs), 1)
        self.assertEquals(len(n.outputs), 2)

    def test_node_2(self):
        n = self.g.get('2')
        self.assertEquals(len(n.inputs), 1)
        self.assertEquals(len(n.outputs), 1)

    def test_node_3(self):
        n = self.g.get('3')
        self.assertEquals(len(n.inputs), 1)
        self.assertEquals(len(n.outputs), 2)

    def test_node_4(self):
        n = self.g.get('4')
        self.assertEquals(len(n.inputs), 3)
        self.assertEquals(len(n.outputs), 1)

    def test_node_5(self):
        n = self.g.get('5')
        self.assertEquals(len(n.inputs), 1)
        self.assertEquals(len(n.outputs), 1)

    def test_node_6(self):
        n = self.g.get('6')
        self.assertEquals(len(n.inputs), 1)
        self.assertEquals(len(n.outputs), 1)

    def test_node_7(self):
        n = self.g.get('7')
        self.assertEquals(len(n.inputs), 2)
        self.assertEquals(len(n.outputs), 0)


class TestGraphScenario2(unittest.TestCase):
    def setUp(self):
        self.g = Graph()
        self.g.add('0')
        self.g.add('1', outputs=['3'])
        self.g.add('2')
        self.g.add('3', inputs=['0', '2'], output='4')
        self.g.add('4', input='0', output='7')
        self.g.add('5', inputs=['3',], output='7')
        self.g.add('6', input='3', outputs=['5', '7'])
        self.g.add('7', inputs=['4', '6'])
        print "setup complete."

    def test_node_0(self):
        n = self.g.get('0')
        self.assertEquals(len(n.inputs), 0)
        self.assertEquals(len(n.outputs), 2)

    def test_node_1(self):
        n = self.g.get('1')
        self.assertEquals(len(n.inputs), 0)
        self.assertEquals(len(n.outputs), 1)

    def test_node_2(self):
        n = self.g.get('2')
        self.assertEquals(len(n.inputs), 0)
        self.assertEquals(len(n.outputs), 1)

    def test_node_3(self):
        n = self.g.get('3')
        self.assertEquals(len(n.inputs), 3)
        self.assertEquals(len(n.outputs), 3)

    def test_node_4(self):
        n = self.g.get('4')
        n.print_edges()
        self.assertEquals(len(n.inputs), 2)
        self.assertEquals(len(n.outputs), 1)

    def test_node_5(self):
        n = self.g.get('5')
        n.print_edges()
        self.assertEquals(len(n.inputs), 2)
        self.assertEquals(len(n.outputs), 1)

    def test_node_6(self):
        n = self.g.get('6')
        self.assertEquals(len(n.inputs), 1)
        self.assertEquals(len(n.outputs), 2)

    def test_node_7(self):
        n = self.g.get('7')
        self.assertEquals(len(n.inputs), 3)
        self.assertEquals(len(n.outputs), 0)