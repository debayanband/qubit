import numpy as np

class Register:

    def __init__(self, qubits):
        """ Initializes a quantum register with QUBITS number of qubits. """

        self.numQubits = qubits

        # There should be 2^n amplitudes with n qubits
        self.amplitudes = np.zeros(2**numQubits)

        # is there anything else?

    def apply(self, gate, *args):
        """ GATE is the gate we wish to apply, 
        and *ARGS is the qubits to which GATE is applied to. """

    def measure(self, qubit, basis):
        """ QUBIT is a list of qubits we wish to measure,
        and BASIS is the set of vectors that we are measuring relative to.
        """
