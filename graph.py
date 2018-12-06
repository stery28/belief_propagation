from copy import deepcopy


class Graph:
    # vertices = []  # List of Nodes
    # edges = []  # Lsit of tuple of Nodes, e.g.: (Node1, Node2) represents the edge Node1 -> Node2
    # directed = True  # Boolean representing if the Graph is directed or not

    def __init__(self, directed):
        self.vertices = []
        self.edges = []
        self.directed = directed

    def add_node(self, node):
        self.vertices.append(node)
        for parent in node.parents:
            self.add_edge(parent, node)

    def add_edge(self, node1, node2):
        self.edges.append((node1, node2))
        if not self.directed:
            self.edges.append((node2, node1))

    def get_node(self, node_name):
        for node in self.vertices:
            if node.name == node_name:
                return node
        return None

    def make_undirected_copy(self):
        undirected_copy = Graph(False)
        undirected_copy.vertices = deepcopy(self.vertices)
        # TODO: Optimize with deepcopy argument/Boolean check, maybe only deepcopy the edges

        for edge in self.edges:
            (node1, node2) = edge
            new_node1, new_node2 = undirected_copy.get_node(node1.name), undirected_copy.get_node(node2.name)

            if new_node1 is None or new_node2 is None:
                print("Error: Could not properly copy a node in make_undirected_copy")
                return None
            undirected_copy.add_edge(new_node1, new_node2)

        return undirected_copy
