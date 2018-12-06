import parser
from node import Node, Factor
from graph import Graph


def build_bayesian_graph(bayesian_vars):
    Phi = Factor([], {})
    # for bayesian_var in bayesian_vars:
    #     # print(list(map(lambda s: s.strip(), bayesian_var.split(";"))))
    #     name, parents, probs = list(map(lambda s: s.strip(), bayesian_var.split(";")))
    #     parents = parents.split()
    #     probs = [float(x) for x in probs.split()]
    #     print(name + "|" + str(parents) + "|" + str(probs))
    print(bayesian_vars)



def main():
    bayesian_vars, required_probabilities, expected_probabilities = parser.read_input()
    build_bayesian_graph(bayesian_vars)


if __name__ == '__main__':
    main()
