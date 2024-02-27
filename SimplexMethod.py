import numpy as np
import math

from MethodExtremePoints import *

class SimplexMethod:
    def __init__(self, c, A, b, changes_dict, x_limits_start):
        new_c = c.copy().elems
        new_A = []
        new_b = b.copy().elems

        for row in A.copy():
            new_A.append(row.copy().elems)

        self.c = new_c
        self.A = new_A
        self.b = new_b
        self.changes_dict = changes_dict
        self.x_limits_start = x_limits_start

        self.tableau = self.to_tableau(new_c, new_A, new_b)

    def to_tableau(self, c, A, b):
        xb = [eq + [x] for eq, x in zip(A, b)]
        z = c + [0]
        return xb + [z]

    def can_be_improved(self):
        z = self.tableau[-1]
        column = None
        for i, x in enumerate(z[:-1]):
            if x < 0:
                column = i
                break
        return column is not None

    def get_pivot_position(self):
        z = self.tableau[-1]
        column = None
        for i, x in enumerate(z[:-1]):
            if x < 0:
                column = i
                break
        restrictions = []
        for eq in self.tableau[:-1]:
            el = eq[column]
            restrictions.append(math.inf if el <= 0 else eq[-1] / el)

        row = restrictions.index(min(restrictions))
        if restrictions[row] == math.inf:
            return -1, -1
        else:
            return row, column

    def pivot_step(self, pivot_position):
        new_tableau = [[] for eq in self.tableau]

        i, j = pivot_position
        pivot_value = self.tableau[i][j]
        new_tableau[i] = np.array(self.tableau[i]) / pivot_value

        for eq_i, eq in enumerate(self.tableau):
            if eq_i != i:
                multiplier = np.array(new_tableau[i]) * self.tableau[eq_i][j]
                new_tableau[eq_i] = np.array(self.tableau[eq_i]) - multiplier

        self.tableau = new_tableau

    def is_basic(self, column):
        return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1

    def get_solution(self):
        columns = np.array(self.tableau).T
        solutions = [] # [1, 3, ...]
        answer = 0
        c_index = 0
        for column in columns:
            solution = 0
            if self.is_basic(column):
                one_index = column.tolist().index(1)
                solution = columns[-1][one_index]
                c_value = self.c[c_index]
                answer += solution * c_value
            c_index += 1
            solutions.append(solution)
        change_target = self.changes_dict.get('CHANGE_TARGET')
        if change_target == 1:
            answer = -answer

        curr_x = []
        for i in range(len(self.x_limits_start)):
            if self.x_limits_start[i] == 1:
                curr_x.append(solutions[i])
            elif self.x_limits_start[i] == -1:
                curr_x.append(solutions[i])
            elif self.x_limits_start[i] == 0:
                temp = solutions[i] - solutions[i + 1]
                curr_x.append(temp)

        print("Оптимальный вектор: ")
        print(curr_x)
        return answer

    def solve(self):
        while self.can_be_improved():
            pivot_position = self.get_pivot_position()
            if pivot_position[0] == -1 and pivot_position[1] == -1:
                return "ПРОСТРАНСТВО ДОПУСТИМЫХ РЕШЕНИЙ НЕОГРАНИЧЕННО: РЕШЕНИЯ ЗАДАЧИ НЕ СУЩЕСТВУЕТ"
            else:
                self.pivot_step(pivot_position)
        return self.get_solution()

# c = [-3, -2, 0, 0, 0]
# A = [
#     [-5, 4, 1, 0, 0],
#     [ 2, 3, 0, 1, 0],
#     [ 1, -3, 0, 0, 1]
# ]
# b = [20, 24, 3]

# c = [-1, -1, 0, 0, 0]
# A = [
#     [1, 2, 1, 0, 0],
#     [2, 1, 0, 1, 0],
#     [-1, -2, 0, 0, 1]
# ]
# b = [10, 10, -2]

# c = [10, -57, -9, -24, 0, 0, 0]
# A = [
#     [0.5, -5.5, -2.5, 9, 1, 0, 0],
#     [0.5, -1.5, -0.5, 1, 0, 1, 0],
#     [1, 0, 0, 0, 0, 0, 1]
# ]
# b = [0, 0, -1]

# c = [-1, 3, -2, 0, 0, 0, 0]
# A = [
#     [1, 1, 0, 1, 0, 0, 0],
#     [2, -1, 1, 0, 1, 0, 0],
#     [-1, 1, 0, 0, 0, 1, 0],
#     [-2, 1, -1, 0, 0, 0, 1]
# ]
# b = [18, 15, -6, -15]
