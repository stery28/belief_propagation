import parser
from lab09 import *
from node import Node
from graph import Graph
from itertools import product, combinations
from copy import deepcopy, copy


def build_bayesian_graph(bayesian_vars):
    Phi = []
    bayesian_graph = Graph(True)

    for bayesian_var in bayesian_vars:
        name, parents, probs = bayesian_var
        phi = Factor([], {})
        phi.vars.append(name)
        for parent in parents:
            phi.vars.append(parent)  # Check if order matters

        # Get all the parents=0/1 combinations
        zipped_values = [list(zip(parents, value)) for value in product(range(2), repeat=len(parents))]
        for combination in enumerate(zipped_values):  # enumerate so we can get the index in probs
            values1 = [1]  # This node's value(current bayesian_var) is 1
            values0 = [0]  # The complement of values1
            for parent in combination[1]:
                values1.append(parent[1])
                values0.append(parent[1])

            phi.values[tuple(values1)] = probs[combination[0]]  # e.g. phi.values[(1,0,1)] = 0.2 is P(X=1|Y=0,Z=1)=0.2
            phi.values[tuple(values0)] = 1 - probs[combination[0]]

        Phi.append(phi)
        node = Node(name, parents, phi)
        bayesian_graph.add_node(node)
    bayesian_graph.compute_edges()
    return bayesian_graph, Phi


def bron_kerbosch(cliques, r, p, x):
    if not p and not x:
        cliques.append(r)
    p_copy = copy(p)  # I was losing values because I was removing from the same list I was iterating through
    for node in p_copy:
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
    for edge in ordered_edges:
        node1, node2 = edge
        group1 = []
        group2 = []
        for group in groups:
            if node1 in group:
                group1 = group
            if node2 in group:
                group2 = group
            if group1 and group2:
                break
        if group1 == group2:
            continue
        group1 += group2
        groups.remove(group2)
        maxspangraph.add_edge(node1, node2)
    return maxspangraph


def gather_messages(root: Node, visited: list):  # DFS so the root can wait for all the messages from its children
    unvisited_children = [child for child in root.children if child not in visited]
    new_phi = None
    for child in unvisited_children:
        visited.append(child)
        message = gather_messages(child, visited)
        root.messages[child.name] = message  # Save the message for step 3.4
        if not new_phi:
            new_phi = message
            continue
        elif message:
            new_phi = multiply_factors(new_phi, message)
    if new_phi and root.factor:
        new_phi = multiply_factors(new_phi, root.factor)
        root.factor = new_phi
    elif new_phi:
        root.factor = new_phi
    if root.factor and root.parent:  # If this Node has a parent and a factor to project
        not_common_vars = [var for var in root.factor.vars if var not in intersect_strings(root.name, root.parent.name)]
        my_message = deepcopy(root.factor)
        for var in not_common_vars:
            my_message = sum_out(var, my_message)
        return my_message
    return None


def scatter_messages(root: Node, parent_message: Factor):
    if root.parent:
        if root.factor and parent_message:
            root.factor = multiply_factors(root.factor, parent_message)
        elif parent_message:
            root.factor = parent_message
    for child in root.children:
        my_message = deepcopy(root.factor)
        inverted_child_message = deepcopy(root.messages[child.name])
        for value in inverted_child_message.values:
            inverted_child_message.values[value] = 1/inverted_child_message.values[value]  # So that we can use multiply
        my_message = multiply_factors(my_message, inverted_child_message)  # phi / message
        not_common_vars = [var for var in my_message.vars if var not in intersect_strings(root.name, child.name)]
        for var in not_common_vars:
            my_message = sum_out(var, my_message)  # Project
        scatter_messages(child, my_message)


def main():
    bayesian_vars, required_probabilities, expected_probabilities = parser.read_input()
    bayesian_graph, Phi = build_bayesian_graph(bayesian_vars)

    # 2.1: Build undirected graph U based on the Bayesian graph G
    undirected_graph = bayesian_graph.make_undirected_copy()

    # 2.2: Build "moral" graph H based on U
    for node in bayesian_graph.nodes.values():
        u_parents = [undirected_graph.get_node(parent_name) for parent_name in node.parents]
        if len(u_parents) < 2:
            continue

        for combo in combinations(u_parents, 2):
            node1, node2 = combo
            if not undirected_graph.check_edge(node1, node2):
                undirected_graph.add_edge(node1, node2)

    # 2.3: Build "chordal" graph H* based on H(the old U)
    copy_graph = deepcopy(undirected_graph)
    sorted_nodes = list(copy_graph.nodes.values())
    sorted_nodes.sort(key=(lambda n: copy_graph.count_not_connected_parents(n.name)))
    while sorted_nodes and copy_graph.count_not_connected_parents(sorted_nodes[-1].name) > 0:
        node = sorted_nodes[0]
        for parents_name_combo in combinations(node.parents, 2):  # check if 2 by 2 parents are connected
            parent_name1, parent_name2 = parents_name_combo
            parent_node1, parent_node2 = copy_graph.nodes[parent_name1], copy_graph.nodes[parent_name2]
            if not copy_graph.check_edge(parent_node1, parent_node2):  # if they are not linked
                copy_graph.add_edge(parent_node1, parent_node2)  # add edge
                # also add it to the H* graph
                undirected_graph.add_edge(undirected_graph.nodes[parent_name1], undirected_graph.nodes[parent_name2])
        copy_graph.remove_node(node.name)
        sorted_nodes = list(copy_graph.nodes.values())
        sorted_nodes.sort(key=(lambda n: copy_graph.count_not_connected_parents(n.name)))

    # 2.4: Build "cliques" graph C using H*
    cliques = []
    bron_kerbosch(cliques, [], list(undirected_graph.nodes.values()), [])  # Extract maximal cliques

    # Create the Graph
    cliques_graph = Graph(False)
    for clique in cliques:  # clique is a list of Nodes
        sorted_nodes_list = [node.name for node in clique]
        sorted_nodes_list.sort()
        node_name = ''.join(sorted_nodes_list)
        node_phi = None
        for phi in Phi:  # Compute a factor for each node in C
            if contains_string(node_name, phi.vars):
                # phi contains only vars from this Node
                if node_phi is None:
                    node_phi = phi
                else:
                    node_phi = multiply_factors(node_phi, phi)

        node = Node(node_name, [], node_phi)
        cliques_graph.add_node(node)
    for nodes_combo in combinations(cliques_graph.nodes.values(), 2):
        node1, node2 = nodes_combo
        edge_name = ''.join(intersect_strings(node1.name, node2.name))
        if edge_name:
            cliques_graph.add_edge(node1, node2)

    # 2.5: Build maximum spanning tree/graph T using Kruskal on C
    maxspangraph = kruskal(cliques_graph)
    maxspangraph.fix_nodes_parents()  # remove nodes that are not neighbours anymore from a Node's parents list
    debug_print_graph(maxspangraph)

    # 2.6: Convert probabilities to factors and associate these factors to each
    # node in the T graph/tree.
    # I've already done that at the 2.4 step

    # 3.1: BFS to create tree hierarchy
    maxspangraph.treeify()

    for prob in required_probabilities:
        copy_graph = deepcopy(maxspangraph)
        # 3.2: Keep only the factors that meet Z = z
        print(prob)
        observed = prob.split("|")[1].strip()
        observed = observed.split()
        observed = [tuple(obs.split("=")) for obs in observed]  # [(val, var)]
        observed = {obs[0]: int(obs[1]) for obs in observed}
        for node in copy_graph.nodes.values():
            if not node.factor:
                continue
            new_factor = condition_factors([node.factor], observed)
            if new_factor:
                node.factor = new_factor[0]
            else:
                node.factor = None

        # 3.3: Send messages from leafs to root
        gather_messages(list(copy_graph.nodes.values())[0], [])
        # 3.4: Send messages from root to leafs
        scatter_messages(list(copy_graph.nodes.values())[0], None)
        # 3.5: Compute required prob
        required_phi = None
        conditions = prob.split("|")[0].strip()
        conditions = conditions.split()
        conditions = [tuple(condition.split("=")) for condition in conditions]
        conditions = {condition[0]: condition[1] for condition in conditions}
        conditions_vars = ''.join(list(conditions.keys()))

        for node in copy_graph.nodes.values():
            if node.factor:
                if contains_string(''.join(node.factor.vars), conditions_vars):
                    # print("Found one")
                    required_phi = deepcopy(node.factor)
                    break
        if not required_phi:
            continue  # Bonus reached
        s = sum(required_phi.values.values())
        required_phi = Factor(required_phi.vars, {k: v / s for k, v in required_phi.values.items()})  # Normalize
        other_vars = [var for var in required_phi.vars if var not in conditions_vars]
        for var in other_vars:
            required_phi = sum_out(var, required_phi)

        required_value = []
        for var in required_phi.vars:
            required_value.append(int(conditions[var]))
        required_value = tuple(required_value)
        print("Required value:", required_phi.values[required_value])
        print("Expected:", expected_probabilities[required_probabilities.index(prob)])


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
