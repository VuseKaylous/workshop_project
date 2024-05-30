from TransformKind import select_transformation

import numpy as np
import sys
import re

"""
Parameters:
    X: The input ndarray
        Shape is [N, 2] where N is the number of ground control points
        X can be in map coordinate or image coordinate
    Y: The desired output
        Shape is [N, 2] where N is the number of ground control points
        Y is map coordinate if X is image coordinate and is image coordinate
        if X is map coordinate
"""
transform_kind = select_transformation()

def find_coefficient(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    X = np.apply_along_axis(transform_kind, 1, X)  # lambda x: [1, x[0], x[1], x[0] * x[0], x[1] * x[0], x[1] * x[1]]
    beta = np.linalg.inv(np.transpose(X) @ X) @ np.transpose(X) @ Y
    return beta

def transform(coeficient, X):
    X = np.apply_along_axis(transform_kind, 1, X)  # lambda x: [1, x[0], x[1], x[0] * x[0], x[1] * x[0], x[1] * x[1]], 1, X)
    return X @ coeficient


print("Input control point in the format (X_in, Y_in) -> (X_out, Y_out)")
parser = re.compile(r"^\s*\(\s*(?P<domain_x>[+-]?\d*(.\d*)?)\s*,\s*(?P<domain_y>[+-]?\d*(.\d*)?)\s*\)\s*->\s*\(\s*(?P<codomain_x>[+-]?\d*(.\d*)?)\s*,\s*(?P<codomain_y>[+-]?\d*(.\d*)?)\s*\)\s*$", re.ASCII)
X, Y = [], []
for line in sys.stdin:
    line = line.replace(" ", "")
    if len(line) == 0:
        continue
    match = parser.match(line)
    if match is None:
        print(line)
        print("Input not in format (X, Y) -> (X, Y)")
        exit()
    else:
        X.append([float(match.group("domain_x")), float(match.group("domain_y"))])
        Y.append([float(match.group("codomain_x")), float(match.group("codomain_y"))])
X, Y = np.array(X, dtype=np.float64), np.array(Y, dtype=np.float64)

forward_coefficient = find_coefficient(X, Y)
backward_coefficient = find_coefficient(Y, X)

np.savez("coefficient.npz", forward=forward_coefficient, backward=backward_coefficient)
print("forward transform: \n", forward_coefficient)
print("backward transform: \n", backward_coefficient)
print("saved to filed coefficient.npz")
