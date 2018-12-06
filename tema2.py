import parser
from node import Node, Factor
from graph import Graph


def build_bayesian_graph(bayesian_vars):
    Phi = Factor([], {})
    for bayesian_var in bayesian_vars:
        print(bayesian_var.split(" ; "))
        name, parents, probs = bayesian_var.split(" ; ")
        print(name, "|", parents, "|", probs)
        print("'"+parents+"'")


def main():
    bayesian_vars, required_probabilities, expected_probabilities = parser.read_input()
    build_bayesian_graph(bayesian_vars)


if __name__ == '__main__':
    main()
