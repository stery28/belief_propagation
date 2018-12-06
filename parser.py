def read_input(path='bn1'):
    input_file = open(path, 'r')
    n, m = [int(x) for x in input_file.readline().split()]
    bayesian_vars = [input_file.readline().rstrip("\n") for _ in range(n)]
    required_probabilities = [input_file.readline().rstrip("\n") for _ in range(m)]
    expected_probabilities = [float(input_file.readline().rstrip("\n")) for _ in range(m)]
    input_file.close()
    return [bayesian_vars, required_probabilities, expected_probabilities]