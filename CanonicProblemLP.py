from GeneralProblemLP import *
from StandartProblemLP import *


class CanonicProblemLP:
    def __init__(self, problem_lp: StandartProblemLP):
        self.C = Vector(problem_lp.C.elems.copy())
        self.target = problem_lp.target
        self.eq_list = problem_lp.eq_list.copy()
        self.gte_list = problem_lp.gte_list.copy()
        self.lte_list = problem_lp.lte_list.copy()
        self.N = problem_lp.N.copy()
        self.basis = []
        self.not_basis = []
        self.constraints_sgn_plus_list = problem_lp.constraints_sgn_plus_list.copy()
        self.constraints_sgn_minus_list = problem_lp.constraints_sgn_minus_list.copy()
        self.x_limits_start = problem_lp.x_limits_start.copy()

        self.A = []
        self.b = []

        self.changes_dict = problem_lp.changes_dict.copy()

        self.change_target_func()
        self.change_lte_to_eq()
        self.change_on_vectors()

    def change_target_func(self):
        C_list = self.C.elems
        if self.lte_list:
            C_list.extend([0 for _ in range(len(self.lte_list))])
        # if self.eq_list:
        #     C_list.extend([0 for _ in range(len(self.eq_list))])
        self.C = Vector(C_list)

    def change_lte_to_eq(self):
        if self.lte_list:
            for i in range(len(self.lte_list)):

                index_new_var = self.N[-1] + 1
                self.basis.append(index_new_var)
                self.N.append(index_new_var)
                self.constraints_sgn_plus_list.append(index_new_var)
                lte = self.lte_list[i]
                b = lte.pop()
                lte.extend([0 for _ in range(len(self.lte_list))])
                lte.append(b)
                lte[index_new_var] = 1.0
                self.eq_list.append(lte)

                self.changes_dict[f'[VARIABLE]: new_variable_{index_new_var}'] = index_new_var

            self.lte_list = []
            self.not_basis = [elem for elem in self.N if elem not in self.basis]
        # if self.eq_list:
        #     for i in range(len(self.eq_list)):
        #         index_new_var = self.N[-1] + 1
        #         self.basis.append(index_new_var)
        #         self.N.append(index_new_var)
        #         self.constraints_sgn_plus_list.append(index_new_var)
        #         eq = self.eq_list[i]
        #         b = eq.pop()
        #         eq.extend([0 for _ in range(len(self.eq_list))])
        #         eq.append(b)
        #         eq[index_new_var] = 1.0
        #         self.eq_list.append(eq)
        #
        #         self.changes_dict[f'[VARIABLE]: new_variable_{index_new_var}'] = index_new_var
        #
        #     self.not_basis = [elem for elem in self.N if elem not in self.basis]

    def change_on_vectors(self):
        vec_list = []
        b_list = []
        for eq in self.eq_list.copy():
            b = eq.pop()
            vec = Vector(eq)
            vec_list.append(vec)
            b_list.append(b)
        self.A = Matrix(vec_list)
        self.b = Vector(b_list)

    def __str__(self):
        def sgn(x):
            if x >= 0:
                return '+'
            return '-'

        type_problem = 'Каноническая задача ЛП:\n'
        target_func = ''
        for i in range(len(self.N) - 1):
            target_func += f' {sgn(self.C[i])} {abs(self.C[i])} * x_{i} '
        target_func += f'{sgn(self.C[len(self.N) - 1])} {abs(self.C[len(self.N) - 1])} * x_{len(self.N) - 1}'
        target_func += f' -> {self.target}\n\n'

        equals = ''
        if self.eq_list:
            for eq in self.eq_list:
                for i in range(len(eq) - 1):
                    equals += f' {sgn(eq[i])} {abs(eq[i])} * x_{i} '
                equals += f' {sgn(eq[len(eq) - 1])} {abs(eq[len(eq) - 1])} * x_{len(eq) - 1}'
                index = self.eq_list.index(eq)

                equals += f' = {sgn(self.b[index])}{abs(self.b[index])}\n'



        # lte = f'Неравенства "меньше или равно":\n{str(self.lte_list)}\n'
        # b = f'Вектор правых частей:\n{self.b}\n'
        csp = f'Номера переменных с ограничением неотрицательности (>= 0):\n{str(self.constraints_sgn_plus_list)}\n'
        csm = f'Номера переменных с ограничением неположительности (<= 0):\n{str(self.constraints_sgn_minus_list)}\n'
        result = type_problem + target_func + equals + csp + csm
        return result



        # equals = f'Равенства:\n{str(self.eq_list)}\n'
        # gte = f'Неравенства "больше или равно":\n{str(self.gte_list)}\n'
        # lte = f'Неравенства "меньше или равно":\n{str(self.lte_list)}\n'
        # b = f'Вектор правых частей:\n{self.b}\n'
        # csp = f'Номера переменных с ограничением неотрицательности:\n{str(self.constraints_sgn_plus_list)}\n'
        # csm = f'Номера переменных с ограничением неположительности:\n{str(self.constraints_sgn_minus_list)}\n'
        # result = type_problem + target_func + equals + gte + lte + b + csp + csm + str(self.changes_dict)
        # return result
