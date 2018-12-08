import parser
from lab09 import *
from node import Node
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
    return bayesian_graph, Phi


def bron_kerbosch(cliques, r, p, x):
    if not p and not x:
        cliques.append(r)
    p_copy = copy(p)  # I was losing values because I was removing from the same list I was iterating through
    for node in p_copy:
        # print(
        #     "going to check for r=", ''.join([n.name for n in r] + [node.name]),
        #     "with new p=", ''.join([n.name for n in p if n.name in node.parents]),
        #     node.name + "'s parents=", [parent for parent in node.parents],
        #     "; current p:", [n.name for n in p]
        # )
        bron_kerbosch(
            cliques,
            r + [node],
            [neigh for neigh in p if neigh.name in node.parents],
            [neigh for neigh in x if neigh.name in node.parents]
        )
        p.remove(node)
        x.append(node)


def intersect_strings(str1, str2):  # get intersection of the two strings
    return [c for c in str1 if c in str2]


def contains_string(str1, str2):  # check if all of str2's chars appear in str1
    result = True
    for c in str2:
        if c not in str1:
            result = False
            break
    return result


def kruskal(graph):
    maxspangraph = Graph(False)
    maxspangraph.nodes = deepcopy(graph.nodes)
    groups = [[node] for node in maxspangraph.nodes.values()]
    ordered_edges = []
    for edge in graph.edges:
        node1, node2 = edge
        if (node2, node1) not in ordered_edges:
            ordered_edges.append(edge)
    ordered_edges.sort(reverse=True, key=(lambda e: len(intersect_strings(e[0].name, e[1].name))))
    print([node1.name + "->" + node2.name for (node1, node2) in ordered_edges])
    for edge in ordered_edges:
        node1, node2 = edge
        group1 = []
        group2 = []
        for group in groups:
            # print(group)
            if node1 in group:
                group1 = group
            if node2 in group:
                group2 = group
            if group1 and group2:
                break
        if group1 == group2:
            continue
        # print(list(map(lambda n: n.name, group1)), list(map(lambda n: n.name, group2)))
        group1 += group2
        groups.remove(group2)
        print([n.name for n in group1])
        maxspangraph.add_edge(node1, node2)
    return maxspangraph


def main():
    bayesian_vars, required_probabilities, expected_probabilities = parser.read_input()
    bayesian_graph, Phi = build_bayesian_graph(bayesian_vars)
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
    bron_kerbosch(cliques, [], list(undirected_graph.nodes.values()), [])  # Extract maximal cliques
    print("\n", undirected_graph, "\n")
    print([''.join([node.name for node in clique]) for clique in cliques])
    # Create the Graph
    cliques_graph = Graph(False)
    for clique in cliques:  # clique is a list of Nodes
        sorted_nodes_list = [node.name for node in clique]
        sorted_nodes_list.sort()
        node_name = ''.join(sorted_nodes_list)
        node_phi = None
        for phi in Phi:  # Compute a factor for each node in C
            # print(node_name, phi.vars, contains_string(node_name, phi.vars))
            if contains_string(node_name, phi.vars):
                # phi contains only vars from this Node
                if node_phi is None:
                    node_phi = phi
                else:
                    node_phi = multiply_factors(node_phi, phi)
        # print(node_phi)
        node = Node(node_name, [], node_phi)
        cliques_graph.add_node(node)
    for nodes_combo in combinations(cliques_graph.nodes.values(), 2):
        node1, node2 = nodes_combo
        edge_name = ''.join(intersect_strings(node1.name, node2.name))
        if edge_name:
            # print(edge_name)
            cliques_graph.add_edge(node1, node2)
    print("\n", cliques_graph)
    cliques_graph.print_edges()
    # debug_print_graph(cliques_graph)

    # 2.5: Build maximum spanning tree/graph T using Kruskal on C
    maxspangraph = kruskal(cliques_graph)
    debug_print_graph(maxspangraph)

    # 2.6: Convert probabilities to factors and associate these factors to each
    # node in the T graph/tree.
    # I've already done that at the 2.4 step


def debug_print_graph(graph, path='graph.txt'):
    output_file = open(path, 'w')
    for node in graph.nodes:
        output_file.write(node + "\n")
    printed_edges = []
    for edge in graph.edges:
        node1, node2 = edge
        if (node2, node1) not in printed_edges:
            printed_edges.append(edge)
            output_file.write(node1.name + " " + node2.name + "\n")
    output_file.close()


if __name__ == '__main__':
    main()
