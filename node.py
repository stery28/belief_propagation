from collections import namedtuple

Factor = namedtuple("Factor", ["vars", "values"])


class Node:
    # name = ''  # This node's name
    # parents = {}  # Dictionary of Nodes
    # factor = None  # Factor with probabilities

    def __init__(self, name, parents, factor):
        self.name = name
        self.parents = parents
        self.factor = factor

    def __eq__(self, node):
        return self.name == node.name

    def __str__(self):
        return "Node Name: " + self.name + \
               ", Parents: " + str(self.parents) + \
               ", Factor: " + str(self.factor)

    # def get_intersect(self, node):  # Dunno what I meant to do
