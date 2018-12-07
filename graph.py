from copy import deepcopy
from itertools import combinations


class Graph:
    # nodes = {} # Dictionary of Nodes where key=Node.name, value=Node
    # edges = []  # Lsit of tuple of Nodes, e.g.: (Node1, Node2) represents the edge Node1 -> Node2
    # directed = True  # Boolean representing if the Graph is directed or not

    def __init__(self, directed):
        self.nodes = {}
        self.edges = []
        self.directed = directed

    def add_node(self, node):
        self.nodes[node.name] = node
        # for parent in node.parents:
        #     self.add_edge(parent, node)

    def add_edge(self, node1, node2):
        self.edges.append((node1, node2))
        if node1.name not in node2.parents:  # also update parents
            node2.parents.append(node1.name)
        if not self.directed:
            self.edges.append((node2, node1))
            if node2.name not in node1.parents:
                node1.parents.append(node2.name)

    def check_edge(self, node1, node2):  # Check if edge=(node1,node2) already exists
        result = (node1, node2) in self.edges
        if not self.directed:
            result |= (node2, node1) in self.edges
        return result

    def get_node(self, node_name):
        return self.nodes[node_name]

    def make_undirected_copy(self):
        undirected_copy = Graph(False)
        undirected_copy.nodes = deepcopy(self.nodes)
        # TODO: Optimize with deepcopy argument/Boolean check, maybe only deepcopy the edges

        for edge in self.edges:
            (node1, node2) = edge
            new_node1, new_node2 = undirected_copy.get_node(node1.name), undirected_copy.get_node(node2.name)
            # each Node's parents list will be a neighbours list
            if new_node2.name not in new_node1.parents:
                new_node1.parents.append(node2.name)

            if new_node1 is None or new_node2 is None:
                print("Error: Could not properly copy a node in make_undirected_copy")
                return None
            undirected_copy.add_edge(new_node1, new_node2)

        return undirected_copy

    def compute_edges(self):
        for node in self.nodes.values():
            for parent in node.parents:
                self.add_edge(self.nodes[parent], node)

    def get_node_parents(self, node_name):
        node = self.nodes[node_name]
        return [self.nodes[parent] for parent in node.parents]

    def remove_node(self, node_name):
        node = self.nodes[node_name]
        self.nodes.pop(node_name)
        self.edges = [edge for edge in self.edges if node not in edge]
        for other_node in self.nodes.values():
            if node.name in other_node.parents:
                other_node.parents.remove(node.name)

    def count_not_connected_parents(self, node_name):
        node = self.nodes[node_name]
        if len(node.parents) < 2:
            return 0
        count = 0
        for parent_names_combo in combinations(node.parents, 2):
            parent_name1, parent_name2 = parent_names_combo
            parent_node1, parent_node2 = self.nodes[parent_name1], self.nodes[parent_name2]
            if not self.check_edge(parent_node1, parent_node2):
                count += 1
        return count

    def __str__(self):
        return str(
            [node.name + ": " +
             str([parent.name for parent in self.nodes.values() if parent.name in node.parents])
             for node in self.nodes.values()
             ])

    def print_edges(self):
        print(
            [
                node1.name + "->" + node2.name
                for node1, node2 in self.edges
            ]
        )
