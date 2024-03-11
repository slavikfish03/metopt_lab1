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
        self.x_limits_start = problem_lp.x_limits_start

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
        self.N = [x for x in range(len(self.A))]
        self.A = self.A.transpose()


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
                gte_list.append(a)
                #self.b.append(problem_lp.C[constraint])
            elif constraint in problem_lp.constraints_sgn_minus_list:
                a = self.A[constraint]
                p = problem_lp.C[constraint]
                a.append(p)
                lte_list.append(a)
                #self.b.append(problem_lp.C[constraint])
            else:
                a = self.A[constraint]
                p = problem_lp.C[constraint]
                a.append(p)
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
        target_func += f' -> {self.target}\n\n'


       # equals = f'Равенства:\n{str(self.eq_list)}\n'
        equals = ''
        if self.eq_list:
            for eq in self.eq_list:
                for i in range(len(eq) - 1):
                    equals += f' {sgn(eq[i])} {abs(eq[i])} * y_{i} '
                equals += f'= {sgn(eq[len(eq) - 1])} {abs(eq[len(eq) - 1])}\n'

        gte = ''
        if self.gte_list:
            for gte_elem in self.gte_list:
                for i in range(len(gte_elem) - 1):
                    gte += f' {sgn(gte_elem[i])} {abs(gte_elem[i])} * y_{i} '
                gte += f'>= {sgn(gte_elem[len(gte_elem) - 1])} {abs(gte_elem[len(gte_elem) - 1])}\n'

        # gte = f'Неравенства "больше или равно":\n{str(self.gte_list)}\n'
        lte = ''
        if self.lte_list:
            for lte_elem in self.lte_list:
                for i in range(len(lte_elem) - 1):
                    lte += f' {sgn(lte_elem[i])} {abs(lte_elem[i])} * y_{i} '
                lte += f'<= {sgn(lte_elem[len(lte_elem) - 1])} {abs(lte_elem[len(lte_elem) - 1])}\n'
        # lte = f'Неравенства "меньше или равно":\n{str(self.lte_list)}\n'
        # b = f'Вектор правых частей:\n{self.b}\n'
        csp = f'Номера переменных с ограничением неотрицательности (>= 0):\n{str(self.constraints_sgn_plus_list)}\n'
        csm = f'Номера переменных с ограничением неположительности (<= 0):\n{str(self.constraints_sgn_minus_list)}\n'
        result = type_problem + target_func + equals + gte + lte + csp + csm
        return result
