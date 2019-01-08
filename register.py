import numpy as np
import gates as g

class Register:

    def __init__(self, num=6):
        """ Initializes a quantum register with NUM number of qubits. """

        self.numQubits = num

        # There should be 2^n amplitudes with n qubits
        self.amplitudes = np.zeros(2**num, dtype=complex)
        self.amplitudes[0] = 1.+0.j

    def addGate(self, gate, *args):
        """
        GATE is the gate we wish to apply, 
        and *ARGS is the qubits to which GATE is applied to.
        """

        # All the single qubit gates
        single = {'I': eye, 'H': had, 'X': ex, 'Y': why, 
                'Z': zee, 'S': phase, 'T': pioneight}

        #All the two qubit gates
        double = {'CNOT': ceenot, 'CX': ceenot,
                'SWAP': swap, 'CZ': ceezee, 'CS': ceephase}

        #All the three qubit gates
        triple = {'TOFFOLI': toff, 'TOFF': toff, 
                'FREDKIN': fred, 'FRED': fred}

        if gate in single:
            applySingle(single[gate], *args)
        elif gate in double:
            applyDouble(double[gate], *args)
        elif gate in triple:
            applyTriple(triple[gate], *args)
        else:
            raise ValueError('{} is not a supported gate. Please try again.'.format(gate))

        def applySingle(func, lst):
            """
            Applies the single qubit gate designated by FUNC
            onto the qubits ennumerated in LST.
            """
            actions = [func() if i+1 in lst else eye(1) for i in range(self.numQubits]
            matrix = g.produceMatrix(actions)
            applyToQubit(matrix)


        def applyDouble(func, q1, q2):
            """
            Applies the two qubit gate designated by FUNC
            onto the qubits at position Q1 and Q2, in that order.
            """
            # TODO: Write up function using swaps.

        def applyTriple(func, q1, q2, q3):
            """
            Applies the three qubit gate designated by FUNC
            onto the qubits at positions Q1, Q2, and Q3 in that order.
            """
            # TODO: Write up function using swaps.

        def applyToQubit(matrix):
            """
            Multiplies the amplitude/state vector by a numpy matrix MATRIX,
            representing the gates applied simultaneously along the register.
            """
            self.amplitudes = matrix @ self.amplitudes



    def measure(self, qubit, basis):
        """ QUBIT is a list of qubits we wish to measure,
        and BASIS is the set of basis states to which the qubits are measured.
        """
        # TODO: Determine a simple way of measuring qubits. 
