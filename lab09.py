# utils from lab09
from copy import deepcopy
from collections import namedtuple

Factor = namedtuple("Factor", ["vars", "values"])


def print_factor(phi, indent="\t"):
    line = " | ".join(phi.vars + ["ϕ(" + ",".join(phi.vars) + ")"])
    sep = "".join(["+" if c == "|" else "-" for c in list(line)])
    print(indent + sep)
    print(indent + line)
    print(indent +sep)
    for values, p in phi.values.items():
        print(indent + " | ".join([str(v) for v in values] + [f"{p:.6f}"]))
    print(indent + sep)


def multiply_factors(phi1, phi2):
    assert isinstance(phi1, Factor) and isinstance(phi2, Factor)
    # Cerinta 1 :
    variables = phi1.vars + [var for var in phi2.vars if var not in phi1.vars]
    result = Factor(variables, {})
    phi1_enum = list(enumerate(phi1.vars))
    phi2_enum = list(enumerate(phi2.vars))
    common_variables = [var for var in phi2.vars if var in phi1.vars]
    for value1, p1 in phi1.values.items():
        for value2, p2 in phi2.values.items():
            # values = []
            # print("Trying tuples " + str(value1) + ", " + str(value2))
            ok = True
            for var in variables:
                if var in common_variables:
                    var_index1 = 0
                    var_index2 = 0
                    for elem in phi1_enum:
                        if elem[1] == var:
                            var_index1 = elem[0]
                            break
                    for elem in phi2_enum:
                        if elem[1] == var:
                            var_index2 = elem[0]
                    # print(var + " " + str(var_index1) + " " + str(var_index2))
                    if value1[var_index1] != value2[var_index2]:
                        ok = False  # values are different for the common variable(s)
                        break
            if not ok:
                continue
            values = list(value1)
            for var in phi2.vars:
                if var in phi1.vars:
                    continue
                var_index = 0
                for elem in phi2_enum:
                    if elem[1] == var:
                        var_index = elem[0]
                        break
                values.append(value2[var_index])
            values = tuple(values)
            # print(str(values) + " " + str(value1) +
            #       " " + str(value2) + " " + str(p1) + " " + str(p2))
            result.values[values] = p1 * p2

    return result


def sum_out(var, phi):
    # print(var, phi)
    assert isinstance(phi, Factor) and var in phi.vars
    # Cerinta 2:
    var_index = 0
    result_variables = [variable for variable in phi.vars if variable != var]
    result = Factor(result_variables, {})
    # phi_enum = list(enumerate(phi.vars))
    for index, variable in enumerate(phi.vars):
        if variable == var:
            var_index = index
            break
    for value, p in phi.values.items():
        new_value = list(value)
        new_value.pop(var_index)
        new_value = tuple(new_value)
        if new_value not in result.values:
            result.values[new_value] = p
        else:
            result.values[new_value] += p
    return result


def prod_sum(var, Phi, verbose=False):
    assert isinstance(var, str) and all([isinstance(phi, Factor) for phi in Phi])
    # Cerinta 3:
    tmp_phi = None
    result = []
    for phi in Phi:
        # print(phi)
        if var not in phi.vars:
            result.append(phi)
            if verbose:
                print(phi)
            continue
        if tmp_phi is None and var in phi.vars:
            tmp_phi = phi
            if verbose:
                print(tmp_phi)
            continue
        if var in phi.vars:
            tmp_phi = multiply_factors(tmp_phi, phi)
            if verbose:
                print(tmp_phi)
        # print(tmp_phi)
    # print(var, tmp_phi)
    if tmp_phi:
        result.append(sum_out(var, tmp_phi))
        if verbose:
            print(sum_out(var, tmp_phi))
    # print(result)

    return result


def variable_elimination(Phi, Z, verbose=False):
    # Cerinta 4:
    result = None
    for z in Z:
        Phi = prod_sum(z, Phi)
    for phi in Phi:
        if result is None:
            result = phi
            continue
        result = multiply_factors(result, phi)
    if verbose:
        print_factor(result)
    return result


def condition_factors(Phi: list, Z: dict, verbose=False):
    # Cerinta 5
    result = []
    for phi in Phi:
        new_phi = Factor(deepcopy(phi.vars), {})
        for value in phi.values:
            ok = True
            for z in Z:
                if z in phi.vars and value[phi.vars.index(z)] != Z[z]:
                    ok = False
                    break
            if not ok:
                continue
            new_phi.values[value] = phi.values[value]
        if len(new_phi.values) > 0:
            result.append(new_phi)
        if verbose:
            print_factor(new_phi)
    return result
