import parser
from node import Node, Factor
from graph import Graph
from itertools import product


def build_bayesian_graph(bayesian_vars):
    Phi = []
    # for bayesian_var in bayesian_vars:
    #     # print(list(map(lambda s: s.strip(), bayesian_var.split(";"))))
    #     name, parents, probs = list(map(lambda s: s.strip(), bayesian_var.split(";")))
    #     parents = parents.split()
    #     probs = [float(x) for x in probs.split()]
    #     print(name + "|" + str(parents) + "|" + str(probs))
    print(bayesian_vars)
    for bayesian_var in bayesian_vars:
        name, parents, probs = bayesian_var
        phi = Factor([], {})
        phi.vars.append(name)
        for parent in parents:
            phi.vars.append(parent)  # Check if order matters
            print(parent)
        parents = ["X","Y","Z"]
        for stuff in product(range(2), repeat=len(parents)):
            print(stuff)
            print(list(zip(parents, stuff)))
        stuff = [list(zip(parents, stuff2)) for stuff2 in product(range(2), repeat=len(parents))]
        print(stuff)  # List of lists with zips



def main():
    bayesian_vars, required_probabilities, expected_probabilities = parser.read_input()
    build_bayesian_graph(bayesian_vars)


if __name__ == '__main__':
    main()
