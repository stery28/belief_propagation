import parser
from node import Node, Factor
from graph import Graph
from itertools import product


def build_bayesian_graph(bayesian_vars):
    Phi = []
    bayesian_graph = Graph(True)
    # for bayesian_var in bayesian_vars:
    #     # print(list(map(lambda s: s.strip(), bayesian_var.split(";"))))
    #     name, parents, probs = list(map(lambda s: s.strip(), bayesian_var.split(";")))
    #     parents = parents.split()
    #     probs = [float(x) for x in probs.split()]
    #     print(name + "|" + str(parents) + "|" + str(probs))
    # print(bayesian_vars)
    for bayesian_var in bayesian_vars:
        name, parents, probs = bayesian_var
        phi = Factor([], {})
        phi.vars.append(name)
        node_parents = {}
        for parent in parents:
            phi.vars.append(parent)  # Check if order matters
            node_parents[parent] = None
            # print(parent)
        # parents = ["X","Y","Z"]
        # for stuff in product(range(2), repeat=len(parents)):
        #     print(stuff)
        #     print(list(zip(parents, stuff)))
        # Get all the parents=0/1 combinations
        zipped_values = [list(zip(parents, value)) for value in product(range(2), repeat=len(parents))]
        # print(zipped_values)  # List of lists with zips
        # print(phi.vars)
        for combination in enumerate(zipped_values):  # enumerate so we can get the index in probs
            values1 = [1]  # This node's value(current bayesian_var) is 1
            values0 = [0]  # The complement of values1
            # print(combination)
            for parent in combination[1]:
                values1.append(parent[1])
                values0.append(parent[1])
            # print(tuple(values))
            phi.values[tuple(values1)] = probs[combination[0]]  # e.g. phi.values[(1,0,1)] = 0.2 is P(X=1|Y=0,Z=1)=0.2
            phi.values[tuple(values0)] = 1 - probs[combination[0]]
            # print(probs[combination[0]])
        Phi.append(phi)
        node = Node(name, node_parents, phi)
        # print(node)
        bayesian_graph.add_node(node)
    bayesian_graph.fix_nodes_parents()
    return bayesian_graph


def main():
    bayesian_vars, required_probabilities, expected_probabilities = parser.read_input()
    bayesian_graph = build_bayesian_graph(bayesian_vars)
    # print("\n\n", bayesian_graph)
    # print(bayesian_graph.edges)
    bayesian_graph.print_edges()  # TODO: REMOVE
    

if __name__ == '__main__':
    main()
