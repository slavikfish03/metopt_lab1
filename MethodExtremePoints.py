import math
from itertools import combinations

from CanonicProblemLP import *
from DualProblemLP import *


class MethodExtremePoints:
    def __init__(self, problem_lp):
        self.N = problem_lp.N.copy()
        self.A = problem_lp.A.copy()
        self.C = problem_lp.C.copy()
        self.b = problem_lp.b.copy()
        self.x_limits_start = problem_lp.x_limits_start.copy()
        self.changes_dict = problem_lp.changes_dict

        self.M = [i for i in range(len(self.A))]
        self.combs = combinations(self.N, len(self.M))

    def combinations_generator(self):
        for comb in self.combs:
            yield comb

    def gauss_method(self, matrix, vector):
        row_list = []
        for row in matrix.rows:
            row_list.append(row.elems)

        matrix = row_list
        vector = vector.elems
        n = len(matrix)
        for i in range(n):
            max_el = abs(matrix[i][i])
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix[k][i]) > max_el:
                    max_el = abs(matrix[k][i])
                    max_row = k

            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            vector[i], vector[max_row] = vector[max_row], vector[i]

            for k in range(i + 1, n):
                c = -matrix[k][i] / matrix[i][i]
                for j in range(i, n):
                    if i == j:
                        matrix[k][j] = 0
                    else:
                        matrix[k][j] += c * matrix[i][j]
                vector[k] += c * vector[i]

        x = [0 for _ in range(n)]
        for i in range(n - 1, -1, -1):
            x[i] = vector[i] / matrix[i][i]
            for k in range(i - 1, -1, -1):
                vector[k] -= matrix[k][i] * x[i]
        for coord in x:
            if coord < 0:
                return 0
        return x

    def back_convert(self, value_opt_tf):
        change_target = self.changes_dict.get('CHANGE_TARGET')
        if change_target:
            value_opt_tf_change = -value_opt_tf
            return value_opt_tf_change
        return value_opt_tf

    def solve(self):
        gen = self.combinations_generator()
        current_opt_value_tf = math.inf
        current_x_opt = [0]
        for N_comb in gen:
            N_comb = list(N_comb)
            A = self.A.copy()[self.M, N_comb]
            A_big = A + self.b # A.copy() must be
            A = self.A.copy()[self.M, N_comb]
            r_A = A.rang()
            r_big = A_big.rang()
            if r_A == r_big:
                gauss_vector = self.gauss_method(A.copy(), self.b.copy())
                if gauss_vector == 0:
                    continue
                support_vector = [0 for _ in range(len(self.N))]
                N_0 = [elem for elem in self.N if elem not in N_comb]
                for i in range(len(self.N)):
                    if i in N_0:
                        support_vector[i] = 0
                    elif i in N_comb:
                        index = N_comb.index(i)
                        support_vector[i] = gauss_vector[index]

                curr_x = []
                for i in range(len(self.x_limits_start)):
                    if self.x_limits_start[i] == 1:
                        curr_x.append(support_vector[i])
                    elif self.x_limits_start[i] == -1:
                        curr_x.append(support_vector[i])
                    elif self.x_limits_start[i] == 0:
                        temp = support_vector[i] - support_vector[i + 1]
                        curr_x.append(temp)

                curr_value_tf = np.dot(self.C.convert_to_np(), np.array(support_vector))
                if curr_value_tf < current_opt_value_tf:
                    current_opt_value_tf = curr_value_tf
                    current_x_opt.pop()
                    current_x_opt.append(curr_x)
        current_opt_value_tf = self.back_convert(current_opt_value_tf)



        return current_x_opt, current_opt_value_tf





