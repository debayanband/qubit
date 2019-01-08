import numpy as np
import gates as g

class Register(object):
    
    def __init__(self, num=6):
        """ Initializes a quantum register with NUM number of qubits. """

        self.numQubits = num

        # There should be 2^n amplitudes with n qubits
        self.amplitudes = np.zeros(2**num, dtype=complex)
        self.amplitudes[0] = 1.+0.j
        
    def addGate(self, gate, lst):
        """
        GATE is the gate we wish to apply, 
        and *ARGS is the qubits to which GATE is applied to.
        """
        
        def applyToQubit(matrix):
            """
            Multiplies the amplitude/state vector by a numpy matrix MATRIX,
            representing the gates applied simultaneously along the register.
            """
            self.amplitudes = matrix @ self.amplitudes

        def applySingle(func, lst):
            """
            Applies the single qubit gate designated by FUNC
            onto the qubits ennumerated in LST.
            """
            actions = [func() if i+1 in lst else g.eye(1) for i in range(self.numQubits)]
            matrix = g.produceMatrix(actions)
            applyToQubit(matrix)


        def applyDouble(func, lst):
            """
            Applies the two qubit gate designated by FUNC
            onto the qubits at position Q1 and Q2, in that order.
            """
            q1 = lst[0]
            q2 = lst[1]
            if q2 == q1+1:
                actions = [g.eye(1) for i in range(self.numQubits - 2)]
                actions.insert(q1-1, func())
                matrix = g.produceMatrix(actions)
                applyToQubit(matrix)
            elif q2 > q1 + 1:
                applyDouble(g.swap, [q2-1, q2])
                applyDouble(func, [q1, q2-1])
                applyDouble(g.swap, [q2-1, q2])
            elif q2 == q1 - 1:
                applyDouble(g.swap, [q2, q1])
                applyDouble(func, [q2, q1])
                applyDouble(g.swap, [q2, q1])
            elif q2 < q1:
                applyDouble(g.swap, [q2, q2+1])
                applyDouble(func, [q1, q2+1])
                applyDouble(g.swap, [q2, q2+1])

        def applyTriple(func, lst):
            """
            Applies the three qubit gate designated by FUNC
            onto the qubits at positions Q1, Q2, and Q3 in that order.
            """
            pass


        # All the single qubit gates
        single = {'I': g.eye, 'H': g.had, 'X': g.ex, 'NOT': g.ex,
                'Y': g.why, 'Z': g.zee, 'S': g.phase, 'T': g.pioneight}

        #All the two qubit gates
        double = {'CNOT': g.ceenot, 'CX': g.ceenot, 
                'SWAP': g.swap, 'CZ': g.ceezee, 'CS': g.ceephase}

        #All the three qubit gates
        triple = {'TOFFOLI': g.toff, 'TOFF': g.toff,
                'FREDKIN': g.fred, 'FRED': g.fred}

        if gate in single:
            applySingle(single[gate], lst)
        elif gate in double:
            applyDouble(double[gate], lst)
        elif gate in triple:
            applyTriple(triple[gate], lst)
        else:
            raise ValueError('{} is not a supported gate. Please try again.'.format(gate))



    def measure(self, qubit, basis):
        """ QUBIT is a list of qubits we wish to measure,
        and BASIS is the set of basis states to which the qubits are measured.
        """
        pass
