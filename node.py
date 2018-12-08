class Node:
    # name = ''  # This node's name
    # parents = []  # List of Node names
    # factor = None  # Factor with probabilities
    # parent = Node  # This Node's parent Node in a tree hierarchy
    # children = [Node]  # List with this Node's children Nodes in a tree hierarchy

    def __init__(self, name, parents, factor):
        self.name = name
        self.parents = parents
        self.factor = factor
        self.parent = None  # for BFS / Tree structure
        self.children = []

    def __eq__(self, node):
        return self.name == node.name

    def __str__(self):
        return "Node Name: " + self.name + \
               ", Parents: " + str(self.parents) + \
               ", Factor: " + str(self.factor) + \
               ", Parent: " + (self.parent.name if self.parent else "None") + \
               ", Children: " + str([child.name for child in self.children])

    # def get_intersect(self, node):  # Dunno what I meant to do
