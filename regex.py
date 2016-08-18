class DFA:
    def __init__(self, d, q0, A):
        self.d = d
        self.A = A
        self.q0 = q0

    def accept(self, input):
        q = self.q0
        for c in input:
            ind = ord(c) - 97
            q = self.d[q][ind]

        return q in self.A


class NFA:
    def __init__(self, d, q0, A):
        self.d = d
        self.A = A
        self.q0 = q0

    def accept(self, input):
        q = self._follow_lambda([self.q0])
        for c in input:
            if not q:
                break
            q_new = []
            ind = ord(c) - 96
            for state in q:
                q_new = q_new + self.d[state][ind]
            q = self._follow_lambda(q_new)

        return bool([x for x in q if x in self.A])

    def _follow_lambda(self, q):
        loop_again = True
        new_states = q
        while loop_again:
            tmp = []
            for state in new_states:
                tmp = tmp + self.d[state][0]
            if not tmp:
                loop_again = False
            else:
                q = q + tmp
                new_states = tmp
        return q


def create_string_NFA(input):
    d = [
        [[] for x in range(27)]
    ]
    last_state = 0
    for c in input:
        ind = ord(c) - 96
        d[last_state][ind].append(last_state + 1)
        d.append([[] for x in range(27)])
        last_state += 1

    return NFA(d, 0, [last_state])


def union_NFA(M1, M2):
    inc_d2 = [[[z + len(M1.d) for z in y] for y in x] for x in M2.d]
    d = M1.d + inc_d2
    d.append([[] for x in range(27)])
    d[len(d) - 1][0] = [M1.q0, M2.q0 + len(M1.d)]
    return NFA(d, len(d) - 1, M1.A + [x + len(M1.d) for x in M2.A])


def kleene_NFA(M):
    d = M.d
    d.append([[] for x in range(27)])
    d[len(d) - 1][0] = [M.q0]
    for state in M.A:
        d[state][0].append(len(d) - 1)
    return NFA(d, len(d) - 1, [len(d) - 1])


def main():
    M = union_NFA(create_string_NFA("what"), create_string_NFA("hello"))
    print M.accept("")


if __name__ == '__main__':
    main()
