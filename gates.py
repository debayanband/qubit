import numpy as np
from scipy.linalg import hadamard

def eye(n=1):
    return np.eye(2**n, dtype=complex)

def had():
    result = hadamard(2, dtype=complex)
    for i in range(2):
        for j in range(2):
            result[i][j] = result[i][j] / np.sqrt(2)
    return result

def ex():
    return np.array([[0.+0.j, 1.+0.j],[1.+0.j, 0.+0.j]])

def why():
    return np.array([[0.+0.j, -1.j],[1.j, 0.+0.j]], dtype=complex)

def zee():
    result = eye(1)
    result[1][1] = -1.+0.j
    return result

def phase(n=1):
    return np.array([[1.+0.j,0.+0.j],[0.+0.j,1.j]], dtype=complex)

def pioneight():
    last_entry = np.array([1.+1.j])
    result = eye(1)
    result[1][1] = last_entry[0]/(np.sqrt(2))
    return result

def ceenot():
    result = eye(2)
    result[2][2] = 0.
    result[2][3] = 1.
    result[3][2] = 1.
    result[3][3] = 0.
    return result

def swap():
    result = eye(2)
    result[1][1] = 0.
    result[1][2] = 1. 
    result[2][1] = 1.
    result[2][2] = 0.
    return result

def ceezee():
    result = eye(2)
    result[3][3] = -1.
    return result

def ceephase():
    result = eye(2)
    result[3][3] = 1.j
    return result

def toff():
    result = eye(3)
    result[6][6] = 0.
    result[6][7] = 1.
    result[7][6] = 1.
    result[7][7] = 0.
    return result

def fred():
    result = eye(3)
    result[5][5] = 0.
    result[5][6] = 1.
    result[6][5] = 1.
    result[6][6] = 0.
    return result

def oplus(a, b):
    return np.kron(a,b)

def produceMatrix(lst):
    a = lst[0]
    for i in range(len(lst) - 1):
        a = oplus(a, lst[i+1])
    return a

