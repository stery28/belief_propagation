import parser
from node import Node, Factor
from graph import Graph
from itertools import product, combinations
from copy import deepcopy, copy


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
        for parent in parents:
            phi.vars.append(parent)  # Check if order matters
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
        node = Node(name, parents, phi)
        # print(node)
        bayesian_graph.add_node(node)
    bayesian_graph.compute_edges()
    return bayesian_graph


def bron_kerbosch(cliques, r, p, x):
    if not p and not x:
        cliques.append(r)
    p_copy = copy(p)  # I was losing values because I was removing from the same list I was iterating through
    for node in p_copy:
        print(
            "going to check for r=", ''.join([n.name for n in r] + [node.name]),
            "with new p=", ''.join([n.name for n in p if n.name in node.parents]),
            node.name + "'s parents=", [parent for parent in node.parents],
            "; current p:", [n.name for n in p]
        )
        bron_kerbosch(
            cliques,
            r + [node],
            [neigh for neigh in p if neigh.name in node.parents],
            [neigh for neigh in x if neigh.name in node.parents]
        )
        p.remove(node)
        x.append(node)


def main():
    bayesian_vars, required_probabilities, expected_probabilities = parser.read_input()
    bayesian_graph = build_bayesian_graph(bayesian_vars)
    # print("\n\n", bayesian_graph)
    # print(bayesian_graph.edges)
    bayesian_graph.print_edges()  # TODO: REMOVE

    # 2.1: Build undirected graph U based on the Bayesian graph G
    undirected_graph = bayesian_graph.make_undirected_copy()
    undirected_graph.print_edges()
    # print("\n", undirected_graph)
    # print(str([parent.name for parent in undirected_graph.get_node_parents("C")]))

    # 2.2: Build "moral" graph H based on U
    for node in bayesian_graph.nodes.values():
        u_parents = [undirected_graph.get_node(parent_name) for parent_name in node.parents]
        if len(u_parents) < 2:
            continue
        # print([node.name for node in u_parents])
        for combo in combinations(u_parents, 2):
            node1, node2 = combo
            if not undirected_graph.check_edge(node1, node2):
                print("Added edge", node1.name, node2.name)
                undirected_graph.add_edge(node1, node2)
                # if node2.name not in node1.parents:
                #     node1.parents.append(node2.name)
                # if node1.name not in node2.parents:
                #     node2.parents.append(node1.name)
    undirected_graph.print_edges()

    # 2.3: Build "chordal" graph H* based on H(the old U)
    copy_graph = deepcopy(undirected_graph)
    sorted_nodes = list(copy_graph.nodes.values())
    sorted_nodes.sort(key=(lambda n: copy_graph.count_not_connected_parents(n.name)))
    print("\n", undirected_graph)
    print([node.name for node in sorted_nodes])
    while sorted_nodes and copy_graph.count_not_connected_parents(sorted_nodes[-1].name) > 0:
        node = sorted_nodes[0]
        print(node.name, copy_graph.count_not_connected_parents(node.name))
        for parents_name_combo in combinations(node.parents, 2):  # check if 2 by 2 parents are connected
            parent_name1, parent_name2 = parents_name_combo
            parent_node1, parent_node2 = copy_graph.nodes[parent_name1], copy_graph.nodes[parent_name2]
            if not copy_graph.check_edge(parent_node1, parent_node2):  # if they are not linked
                copy_graph.add_edge(parent_node1, parent_node2)  # add edge
                # also add it to the H* graph
                undirected_graph.add_edge(undirected_graph.nodes[parent_name1], undirected_graph.nodes[parent_name2])
                # if parent_node1.name not in parent_node2.parents:
                #     parent_node2.parents.append(parent_node1.name)  # update each neighbours/parents
                # if parent_node2.name not in parent_node1.parents:
                #     parent_node1.parents.append(parent_node2.name)
        copy_graph.remove_node(node.name)
        sorted_nodes = list(copy_graph.nodes.values())
        sorted_nodes.sort(key=(lambda n: copy_graph.count_not_connected_parents(n.name)))
    print(copy_graph)
    print("\n", undirected_graph)
    undirected_graph.print_edges()

    # 2.4: Build "cliques" graph C using H*
    cliques = []
    bron_kerbosch(cliques, [], list(undirected_graph.nodes.values()), [])
    print("\n", undirected_graph, "\n")
    print([''.join([node.name for node in clique]) for clique in cliques])


if __name__ == '__main__':
    main()
