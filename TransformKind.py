def linear(x):
    return [x[0], x[1]]

def poly1(x):
    return [1, x[0], x[1]]

def poly2(x):
    return [1, x[0], x[1], x[0] * x[0], x[1] * x[0], x[1] * x[1]]

def poly3(x):
    return [1, x[0], x[1], x[0] * x[0], x[1] * x[0], x[1] * x[1], x[0] * x[0] * x[0], x[1] * x[0] * x[0], x[1] * x[1] * x[0], x[1] * x[1] * x[1]]

def select_transformation():
    transform_kind = input("Select transformation kind: ")
    if transform_kind.lower() == "linear":
        transform_kind = linear
    elif transform_kind.lower() == "polynomial 1":
        transform_kind = poly1
    elif transform_kind.lower() == "polynomial 2":
        transform_kind = poly2
    elif transform_kind.lower() == "polynomial 3":
        transform_kind = poly3
    else:
        print("ERROR: Not recognize transformation kind (", transform_kind, ")")
        exit()
    return transform_kind
