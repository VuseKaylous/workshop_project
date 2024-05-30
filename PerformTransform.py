from TransformKind import select_transformation

import numpy as np
from scipy import interpolate
import cv2

transform_kind = select_transformation()

interpolation_kind = input("Select interpolation kind: ").lower()

def transform(coefficient, X):
    X = np.apply_along_axis(transform_kind, -1, X)
    return X @ coefficient


coefficient_filepath = input("coefficient file: ").strip()
input_image_filepath = input("input image file: ").strip()
viewport = input("output size (topleft_x topleft_y bottomright_x bottomright_y width height): ").strip()
topleft_x, topleft_y, bottomright_x, bottomright_y, out_width, out_height = viewport.strip().split()
topleft_x = float(topleft_x)
topleft_y = float(topleft_y)
bottomright_x = float(bottomright_x)
bottomright_y = float(bottomright_y)
out_height = int(out_height)
out_width = int(out_width)

input_image = cv2.imread(input_image_filepath)
input_image = np.swapaxes(input_image, 0, 1)
(width, height, channel) = input_image.shape

coefficient_forward = None
coefficient_backward = None
with np.load(coefficient_filepath) as coefficient:
    coefficient_forward = coefficient["forward"]
    coefficient_backward = coefficient["backward"]
# print(transform(coefficient_forward, [0, 0]), "  ", transform(coefficient_backward, transform(coefficient_forward, [0, 0])))

grid = np.stack(np.meshgrid(np.linspace(topleft_x, bottomright_x, out_width), np.linspace(topleft_y, bottomright_y, out_height), indexing='ij'),
                -1)
grid = transform(coefficient_backward, grid)
output = interpolate.interpn((np.linspace(0, width - 1, width), np.linspace(0, height - 1, height)), input_image, grid, bounds_error=False,
                             fill_value=0, method=interpolation_kind)
output = np.swapaxes(output, 0, 1)

cv2.imwrite("Output.png", output)
