from itertools import combinations

from CanonicProblemLP import *
from DualProblemLP import *


class MethodExtremePoints:
    def __init__(self, problem_lp):
        self.N = problem_lp.N.copy()
        self.A = problem_lp.A.copy()
        self.C = problem_lp.C.copy()
        self.b = problem_lp.b.copy()

        self.M = [i for i in range(len(self.A))]
        self.combs = combinations(self.N.elems, len(self.M) - len(self.N))

    def combinations_generator(self):
        for comb in self.combs:
            yield comb

    def gauss_method(self):
        pass

    def solve(self):
        N_comb = self.combinations_generator()
        A = self.A[self.M, N_comb]
        



