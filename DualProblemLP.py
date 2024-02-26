from CanonicProblemLP import *


class DualProblemLP:
    def __init__(self, problem_lp: GeneralProblemLP):
        # self.C = problem_lp.C
        # self.target = problem_lp.target
        # self.eq_list = problem_lp.eq_list
        # self.gte_list = problem_lp.gte_list
        # self.lte_list = problem_lp.lte_list
        # self.N = problem_lp.N
        # self.M = len(problem_lp.eq_list) + len(problem_lp.lte_list) + len(problem_lp.gte_list)
        # self.constraints_sgn_plus_list = problem_lp.constraints_sgn_plus_list
        # self.constraints_sgn_minus_list = problem_lp.constraints_sgn_minus_list

        self.C = None
        self.b = []
        self.target = None
        self.constraints_sgn_plus_list = []
        self.constraints_sgn_minus_list = []
        self.A = None
        self.N = None

        self.eq_list = []
        self.gte_list = []
        self.lte_list = []

        self.to_dual(problem_lp)

    def to_dual(self, problem_lp: GeneralProblemLP):
        b_list = []
        eq_list = []
        gte_list = []
        lte_list = []

        for eq in problem_lp.eq_list.copy():
            b_elem = eq.pop()
            b_list.append(b_elem)
            eq = Vector(eq)
            eq_list.append(eq)
        for gte in problem_lp.gte_list.copy():
            b_elem = gte.pop()
            b_list.append(b_elem)
            gte = Vector(gte)
            gte_list.append(gte)
        for lte in problem_lp.lte_list.copy():
            b_elem = lte.pop()
            b_list.append(b_elem)
            lte = Vector(lte)
            lte_list.append(lte)

        self.C = Vector(b_list)
        #self.b = problem_lp.C

        if problem_lp.target == 'max':
            self.target = 'min'
        else:
            self.target = 'max'

        matrix = eq_list + gte_list + lte_list
        self.A = Matrix(matrix)
        self.A = self.A.transpose()
        self.N = [x for x in range(len(self.A))]

        for i in range(len(eq_list) + len(gte_list) + len(lte_list)):
            if 0 <= i < len(eq_list):
                continue
            elif len(eq_list) <= i < (len(gte_list) + len(eq_list)):
                self.constraints_sgn_minus_list.append(i)
            elif len(gte_list) <= i < (len(lte_list) + len(eq_list) + len(gte_list)):
                self.constraints_sgn_plus_list.append(i)



        eq_list = []
        gte_list = []
        lte_list = []

        for constraint in problem_lp.N:
            if constraint in problem_lp.constraints_sgn_plus_list:
                a = self.A[constraint]
                p = problem_lp.C[constraint]
                a.append(p)
                print(a)
                gte_list.append(a)
                #self.b.append(problem_lp.C[constraint])
            elif constraint in problem_lp.constraints_sgn_minus_list:
                a = self.A[constraint]
                p = problem_lp.C[constraint]
                a.append(p)
                print(a)
                lte_list.append(a)
                #self.b.append(problem_lp.C[constraint])
            else:
                a = self.A[constraint]
                p = problem_lp.C[constraint]
                a.append(p)
                print(a)
                eq_list.append(a)
                #self.b.append(problem_lp.C[constraint])

        self.eq_list = eq_list
        self.gte_list = gte_list
        self.lte_list = lte_list



    def __str__(self):
        def sgn(x):
            if x >= 0:
                return '+'
            return '-'

        type_problem = 'Двойственная (к общей) задача ЛП:\n'
        target_func = ''
        for i in range(len(self.C) - 1):
            target_func += f' {sgn(self.C[i])} {abs(self.C[i])} * y_{i} '
        target_func += f'{sgn(self.C[len(self.C) - 1])} {abs(self.C[len(self.C) - 1])} * y_{len(self.C) - 1}'
        target_func += f' -> {self.target}\n'
        equals = f'Равенства:\n{str(self.eq_list)}\n'
        gte = f'Неравенства "больше или равно":\n{str(self.gte_list)}\n'
        lte = f'Неравенства "меньше или равно":\n{str(self.lte_list)}\n'
        b = f'Вектор правых частей:\n{self.b}\n'
        csp = f'Номера переменных с ограничением неотрицательности:\n{str(self.constraints_sgn_plus_list)}\n'
        csm = f'Номера переменных с ограничением неположительности:\n{str(self.constraints_sgn_minus_list)}\n'
        result = type_problem + target_func + equals + gte + lte + b + csp + csm
        return result
