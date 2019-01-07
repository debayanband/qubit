import numpy as np

class Qubit:
    # Common States
    _zero = np.matrix('1; 0')
    _one = np.matrix('0; 1')
    _plus = (1 / sqrt(2)) * np.matrix('1; 1')
    _minus =(1 / sqrt(2)) * np.matrix('1; -1')

    # Represent a qubit state as |\psi > = alpha |0> + beta |1>

    def __init__(self, alpha = np.complex(1, 0), beta = np.complex(0, 0)):
        """ Initializes the qubit. By default inits to state |0>. """
        
        self.alpha = alpha
        self.beta = beta
        self.state = np.matrix([self.alpha, self.beta])

    def state(self):
        """ Returns the qubit as a vector (technically matrix i guess). """
        return self.state

class Gate:
    _i = np.complex(0, 1)

    # 1-qubit gates
    H = (1/sqrt(2)) * np.matrix('1 1; 1 -1')
    X = np.matrix('0 1; 1 0')
    Y = np.matrix([[0, -_i], [_i, 0]])
    Z = np.matrix([[1,0], [0,-1]])
    identity = np.eye(2, 2)

    # This CNOT treats first qubit as control and second as target
    CNOT = np.matrix('1 0 0 0; 0 1 0 0; 0 0 0 1; 0 0 1 0')

    def __init__(self, a = 1, b = 0, c = 0, d = 1):
        """Creates an arbitary gate based on what's passed in.
        Can only create 1 qubit gates.
        Probably not very useful?
        """
        self.matrix = np.matrix([[a, b], [c, d]])



