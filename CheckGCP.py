from TransformKind import select_transformation

import numpy as np
import sys
import re

transform_kind = select_transformation()
def transform(coeficient, X):
    X = np.apply_along_axis(transform_kind, -1, X)  # lambda x: [1, x[0], x[1], x[0] * x[0], x[1] * x[0], x[1] * x[1]], 1, X)
    return X @ coeficient


coefficient_filepath = input("coefficient file: ").strip()
coefficient_forward = None
coefficient_backward = None
with np.load(coefficient_filepath) as coefficient:
    coefficient_forward = coefficient["forward"]
    coefficient_backward = coefficient["backward"]

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

def check_points(coefficient, X, Y):
    Y_hat = transform(coefficient, X)
    return Y_hat - Y


print("Forward error: \n", check_points(coefficient_forward, X, Y))
print("Backward error: \n", check_points(coefficient_backward, Y, X))
