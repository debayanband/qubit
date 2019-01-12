import numpy as np

def zero():
    return np.array([[1.+0.j, 0.+0.j],
                    [0.+0.j, 0.+0.j]])

def one():
    return np.array([[0.+0.j, 0.+0.j],
                    [0.+0.j, 1.+0.j]])

def plus():
    return np.array([[0.5+0.j, 0.5+0.j],
                    [0.5+0.j, 0.5+0.j]])

def minus():
    return np.array([[0.5+0.j, -0.5+0.j],
                    [-0.5+0.j, 0.5+0.j]])

def pos_y():
    return np.array([[0.5+0.j, 0.+0.5j],
                    [0.+0.5j, -0.5+0.j]])

def neg_y():
    return np.array([[0.5+0.j, 0.-0.5j],
                    [0.-0.5j, -0.5+0.j]])

