def read_input(path='bn1'):
    input_file = open(path, 'r')
    n, m = [int(x) for x in input_file.readline().split()]
    tmp_bayesian_vars = [input_file.readline().rstrip("\n") for _ in range(n)]
    required_probabilities = [input_file.readline().rstrip("\n") for _ in range(m)]
    expected_probabilities = [float(input_file.readline().rstrip("\n")) for _ in range(m)]

    bayesian_vars = []
    for bayesian_var in tmp_bayesian_vars:
        name, parents, probs = list(map(lambda s: s.strip(), bayesian_var.split(";")))
        parents = parents.split()
        probs = [float(x) for x in probs.split()]
        bayesian_vars.append((name, parents, probs))

    input_file.close()
    return [bayesian_vars, required_probabilities, expected_probabilities]