import numpy as np
from numpy import linalg as la
import gates as g
import random as r
import measurement_operators as mops

class Register(object):
    
    def __init__(self, num=8):
        """ Initializes a quantum register with NUM number of qubits. """
        self.numQubits = num

        # For an n-qubit register, there are 2^n basis states
        self.amplitudes = np.zeros(2**num, dtype=complex)
        self.amplitudes[0] = 1.+0.j # Initializes to the |000...0> state
        
    def addGate(self, gate, lst):
        """
        GATE is the gate we wish to apply, 
        and *ARGS is the qubits to which GATE is applied to.
        """
        
        def applyToQubit(matrix):
            """
            Multiplies the amplitude/state vector by a numpy matrix MATRIX,
            representing the gates applied simultaneously along the register.
            Note that this matrix is unitary and of size 2^n by 2^n.
            """
            self.amplitudes = matrix @ self.amplitudes

        def applySingle(func, lst):
            """
            Applies the single qubit gate designated by FUNC
            onto the qubits ennumerated in LST.
            
            Note that produceMatrix "lifts" single qubit gates to represent 
            a tensor product of operations onto every qubit in the register.
            """
            actions = [func() if i+1 in lst else g.eye(1) 
                    for i in range(self.numQubits)]
            matrix = g.produceMatrix(actions)
            applyToQubit(matrix)


        def applyDouble(func, lst):
            """
            Applies the two qubit gate designated by FUNC
            onto the qubits at position Q1 and Q2, in that order.
            Note that our "lifting" method only works for adjacent qubits.
            Thus, we must do a sequence of swaps before applying our gate,
            and then perform those swaps in reverse order.
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

        def group(i, j, k): # Helper function for applyTriple
            """
            Moves qubits at positions I, J, K until they are adjacent.
            """
            while ((i != j-1) and (k != j+1)):
                actions = [g.eye(1) for i in range(self.numQubits - 4)]
                actions.insert(i-1, swap())
                actions.insert(k-3, swap())
                matrix = g.produceMatrix(actions)
                applyToQubits(matrix)
                i = i + 1
                k = k - 1
            if ((i == j-1) and (k == j+1)):
                return
            elif ((i == j-1) and (k > j+1)):
                while (k != j+1):
                    applyDouble(g.swap, [k-1, k])
                    k = k-1
                return
            else:
                while (i != j-1):
                    applyDouble(g.swap, [i, i+1])
                    i = i+1
                return

        def ungroup(i, j, k): # Helper function for applyTriple
            """
            From the previously grouped position, swap each qubit back
            to its respective initial position, indices I, J, K.
            """
            l = j - 1
            m = j + 1
            while ((l != i) and (m != j)):
                actions = [g.eye(1) for i in range(self.numQubits - 4)]
                actions.insert(l-2, swap())
                actions.insert(m-2, swap())
                matrix = g.produceMatrix(actions)
                applyToQubits(matrix)
                l = l - 1
                m = m + 1
            if ((l == i) and (m == j)):
                return
            elif ((l == i) and (m < j)):
                while (m < j):
                    applyDouble(g.swap, [m, m+1])
                    m = m + 1
                return
            else:
                while (l > i):
                    applyDouble(g.swap, [l-1, l])
                    l = l-1
                return

        def applyTriple(func, lst):
            """
            Applies the three qubit gate designated by FUNC
            onto the qubits at positions Q1, Q2, and Q3 in that order.
            """
            q1 = lst[0]
            q2 = lst[1]
            q3 = lst[2]
            if ((q2 == q1+1) and (q3 == q2+1)):
                actions = [g.eye(1) for i in range(self.numQubits - 3)]
                actions.insert(q1-1, func())
                matrix = g.produceMatrix(actions)
                applyToQubit(matrix)
            elif (abs(q3 - q2) + abs(q2 - q1) <= 3):
                if ((q3 == q1 + 1) and (q2 == q3+1)):
                    applyDouble(g.swap, [q3, q2])
                    applyTriple(func, [q1, q3, q2])
                    applyDouble(g.swap, [q3, q2])
                elif ((q3 == q2 + 1) and (q1 == q3 + 1)):
                    applyDouble(g.swap, [q3, q1])
                    applyDouble(g.swap, [q2, q3])
                    applyTriple(func, [q2, q3, q1])
                    applyDouble(g.swap, [q2, q3])
                    applyDouble(g.swap, [q3, q1])
                elif ((q1 == q2 + 1) and (q3 == q1 + 1)):
                    applyDouble(g.swap, [q2, q1])
                    applyTriple(func, [q2, q1, q3])
                    applyDouble(g.swqp, [q2, q1])
                elif ((q2 == q3 + 1) and (q1 == q2 + 1)):
                    applyDouble(g.swap, [q3, q2])
                    applyDouble(g.swap, [q2, q1])
                    applyDouble(g.swap, [q3, q2])
                    applyTriple(func, [q3, q2, q1])
                    applyDouble(g.swap, [q3, q2])
                    applyDouble(g.swap, [q2, q1])
                    applyDouble(g.swap, [q3, q2])
                elif ((q1 == q3 + 1) and (q2 == q1 + 1)):
                    applyDouble(g.swap, [q3, q1])
                    applyDouble(g.swap, [q1, q2])
                    applyTriple(func, [q3, q1, q2])
                    applyDouble(g.swap, [q1, q2])
                    applyDouble(g.swap, [q3, q1])
            else:
                if ((q1 < q2) and (q2 < q3)):
                    group(q1, q2, q3)
                    applyTriple(func, [q2-1, q2, q2+1])
                    ungroup(q1, q2, q3)
                elif ((q1 < q3) and (q3 < q2)):
                    group(q1, q3, q2)
                    applyTriple(func, [q3-1, q3+1, q3])
                    ungroup(q1, q3, q2)
                elif ((q2 < q1) and (q1 < q3)):
                    group(q2, q1, q3)
                    applyTriple(func, [q1, q1-1, q1+1])
                    ungroup(q2, q1, q3)
                elif ((q2 < q3) and (q3 < q1)):
                    group(q2, q3, q1)
                    applyTriple(func, [q3+1, q3-1, q3])
                    ungroup(q2, q3, q1)
                elif ((q3 < q1) and (q1 < q2)):
                    group(q3, q1, q2)
                    applyTriple(func, [q1, q1+1, q1-1])
                    ungroup(q3, q1, q2)
                elif ((q3 < q2) and (q2 < q1)):
                    group(q3, q2, q1)
                    applyTriple(func, [q2+1, q2, q2-1])
                    ungroup(q3, q2, q1)


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
            raise ValueError('{} is not a supported gate.'.format(gate))

    def measure(self, qstr, lst = None, sampling = False):
        """ 
        QSTR is the string representing measurements to be done on each
        qubit. 'Z' is a standard basis measurement, 'X' is a Hadamard
        basis measurement, 'Y' is a measurement in the Y basis states,
        and 'I' is the identity (i.e. no measurement on that qubit).
        """
    
        def generateLst(measureNum):
            """
            Generates a list of strings, composed of '0' and '1' chars,
            that represent all the permutations of MEASURENUM bits,
            in binary number order. 
            """
            stringLst = ['0'*measureNum]
            count = 1
            while (count < 2**measureNum):
                addedOne = False
                prevString = stringLst[count - 1]
                toAddString = ''
                while (len(toAddString) < measureNum):
                    innerCount = len(toAddString)
                    if addedOne:
                        prepend = prevString[:(measureNum - innerCount)]
                        toAddString = prepend + toAddString
                    else:
                        if prevString[measureNum - innerCount - 1] == '0':
                            toAddString = '1' + toAddString
                            addedOne = True
                        else:
                            toAddString = '0' + toAddString
                stringLst.append(toAddString)
                count += 1
            return stringLst
        
        qstr = ''.join(qstr.split())
        qstr = qstr.upper()
        num = qstr.count('X') + qstr.count('Y') + qstr.count('Z')
        if lst is None:
            lst = generateLst(num)
        final = ''
        tryOp = r.randint(0, 2**num - 1)
        measured = False
        while not measured:
            guide = lst[tryOp]
            if isinstance(guide, str):
                index = 0
                matrixLst = []
                for i in range(self.numQubits):
                    if qstr[i] == 'X':
                        if guide[index] == '0':
                            matrixLst.append(mops.plus())
                            index += 1
                            final = final + '|+>'
                        else: 
                            matrixLst.append(mops.minus())
                            index += 1
                            final = final + '|->'
                    elif qstr[i] == 'Y':
                        if guide[index] == '0':
                            matrixLst.append(mops.pos_y())
                            index += 1
                            final = final + '|i>'
                        else:
                            matrixLst.append(mops.neg_y())
                            index += 1
                            final = final + '|-i>'
                    elif qstr[i] == 'Z':
                        if guide[index] == '0':
                            matrixLst.append(mops.zero())
                            index += 1
                            final = final + '|0>'
                        else:
                            matrixLst.append(mops.one())
                            index += 1
                            final = final + '|1>'
                    else:
                        matrixLst.append(g.eye(1))
                        final = final + '|psi_' + str(i+1) + '>'
                measureMatrix = g.produceMatrix(matrixLst)
                collapsed = measureMatrix @ self.amplitudes
                lst[tryOp] = (collapsed, final)
                ampnorm = la.norm(collapsed)
                prob = (ampnorm)**2
                spinner = r.random()
                if spinner <= prob:
                    for i in range(2**self.numQubits):
                        collapsed[i] = collapsed[i] / ampnorm
                    self.amplitudes = collapsed
                    measured = True
                    if sampling:
                        return final, lst
                    return final
                else:
                    tryOp = r.randint(0, 2**num - 1)
                    final = ''

            else: 
                collapsed = guide[0]
                ampnorm = la.norm(collapsed)
                prob = (ampnorm)**2
                spinner = r.random()
                if r.random() <= prob:
                    for i in range(2**self.numQubits):
                        collapsed[i] = collapsed[i] / ampnorm
                    self.amplitudes = collapsed
                    measured = True
                    if sampling:
                        return guide[1], lst
                    return guide[1]
                else:
                    tryOp = r.randint(0, 2**num - 1)

    def sample(self, qstr, samples):
        """
        Like measuring, but does it SAMPLES amount of times.
        Prints what result is measured how many times.
        """
        amps = self.amplitudes
        results = {}
        lst = None
        for _ in range(samples):
            result, lst = self.measure(qstr, lst, True)
            self.amplitudes = amps
            if result in results:
                results[result] += 1
            else:
                results[result] = 1

        for result in results:
            print(f"We measured {result} {results[result]} times.")
