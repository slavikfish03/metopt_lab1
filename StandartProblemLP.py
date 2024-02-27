from GeneralProblemLP import *


class StandartProblemLP:
    def __init__(self, problem_lp):
        self.C = Vector(problem_lp.C.elems.copy())
        self.target = problem_lp.target
        self.x_limits_start = problem_lp.x_limits_start

        self.eq_list = []
        for eq in problem_lp.eq_list:
            self.eq_list.append(eq.copy())

        self.gte_list = []
        for gte in problem_lp.gte_list:
            self.gte_list.append(gte.copy())

        self.lte_list = []
        for lte in problem_lp.lte_list:
            self.lte_list.append(lte.copy())

        self.N = problem_lp.N.copy()
        self.constraints_sgn_plus_list = problem_lp.constraints_sgn_plus_list.copy()
        self.constraints_sgn_minus_list = problem_lp.constraints_sgn_minus_list.copy()

        self.changes_dict = {}

        self.change_target()
        self.change_constraints_minus()
        self.change_eq_to_ineq()
        self.change_not_constraints()
        self.change_gte_to_lte()
        self.change_vars()

    def change_target(self):
        if self.target == 'max':
            self.target = 'min'
            self.changes_dict['CHANGE_TARGET'] = 1
            self.C = -1 * self.C

    def change_constraints_minus(self):
        if self.constraints_sgn_minus_list:
            for num_constraint in self.constraints_sgn_minus_list:
                self.C[num_constraint] = -1 * self.C[num_constraint]
                self.changes_dict[f'[VARIABLE]: is_variable_{num_constraint}_change_sgn'] = 1
                for eq in self.eq_list:
                    eq[num_constraint] = -1 * eq[num_constraint]
                for gte in self.gte_list:
                    gte[num_constraint] = -1 * gte[num_constraint]
                for lte in self.lte_list:
                    lte[num_constraint] = -1 * lte[num_constraint]
                self.constraints_sgn_plus_list.append(num_constraint)
            self.constraints_sgn_minus_list = []

    def change_eq_to_ineq(self):
        for i in range(len(self.eq_list)):
            eq = self.eq_list.pop(0)
            self.lte_list.append(eq.copy())
            self.gte_list.append(eq.copy())
        self.eq_list = []

    def change_not_constraints(self):
        not_constraints_list = [num for num in self.N if num not in self.constraints_sgn_plus_list]
        for not_constraint in not_constraints_list:
            # X = X' - X'', X' >= 0, X'' >= 0
            coeff = self.C[not_constraint]
            self.C[not_constraint] = [coeff, -coeff]
            self.changes_dict[f'[VARIABLE]: is_new_var_{not_constraint}_streak X_{not_constraint} =' \
                              f' X"_{not_constraint} - X""_{not_constraint}'] = not_constraint

            for i in range(len(self.gte_list)):
                coeff_gte = self.gte_list[i][not_constraint]
                self.gte_list[i][not_constraint] = [coeff_gte, -coeff_gte]

            for i in range(len(self.lte_list)):
                coeff_lte = self.lte_list[i][not_constraint]
                self.lte_list[i][not_constraint] = [coeff_lte, -coeff_lte]
            # for lte in self.lte_list:
            #     coeff_lte = lte[not_constraint]
            #     lte[not_constraint] = [coeff_lte, -coeff_lte]

            self.constraints_sgn_plus_list.append([not_constraint])

    def change_gte_to_lte(self):
        for gte_expression in self.gte_list:
            for i in range(len(gte_expression)):
                if not isinstance(gte_expression[i], List):
                    gte_expression[i] = -gte_expression[i]
                else:
                    gte_expression[i] = [-gte_expression[i][x] for x in range(len(gte_expression[i]))]

            self.lte_list.append(gte_expression)
        self.gte_list = []

    def change_vars(self):
        C_list = self.C.elems
        C_list_merge = []
        count_replaces = 0
        for C_elem in C_list:
            if isinstance(C_elem, list):
                C_list_merge.extend(C_elem)
                count_replaces += 1
            else:
                C_list_merge.append(C_elem)
        self.C = Vector(C_list_merge)

        if self.lte_list:
            for i in range(len(self.lte_list)):
                lte = self.lte_list[i]
                lte_merge = []
                for lte_elem in lte:
                    if isinstance(lte_elem, list):
                        lte_merge.extend(lte_elem)
                    else:
                        lte_merge.append(lte_elem)
                self.lte_list[i] = lte_merge

        # if self.eq_list:
        #     for i in range(len(self.eq_list)):
        #         eq = self.eq_list[i]
        #         eq_merge = []
        #         for eq_elem in eq:
        #             if isinstance(eq_elem, list):
        #                 eq_merge.extend(eq_elem)
        #             else:
        #                 eq_merge.append(eq_elem)
        #         self.eq_list[i] = eq_merge

        self.constraints_sgn_plus_list = [i for i in range(count_replaces + len(self.N))]
        self.N = self.constraints_sgn_plus_list.copy()

    def __str__(self):
        def sgn(x):
            if x >= 0:
                return '+'
            return '-'

        type_problem = 'Стандартная задача ЛП:\n'
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
                equals += f'= {sgn(eq[len(eq) - 1])} {abs(eq[len(eq) - 1])}\n'

        gte = ''
        if self.gte_list:
            for gte_elem in self.gte_list:
                for i in range(len(gte_elem) - 1):
                    gte += f' {sgn(gte_elem[i])} {abs(gte_elem[i])} * x_{i} '
                gte += f'>= {sgn(gte_elem[len(gte_elem) - 1])} {abs(gte_elem[len(gte_elem) - 1])}\n'

        # gte = f'Неравенства "больше или равно":\n{str(self.gte_list)}\n'
        lte = ''
        if self.lte_list:
            for lte_elem in self.lte_list:
                for i in range(len(lte_elem) - 1):
                    lte += f' {sgn(lte_elem[i])} {abs(lte_elem[i])} * x_{i} '
                lte += f'<= {sgn(lte_elem[len(lte_elem) - 1])} {abs(lte_elem[len(lte_elem) - 1])}\n'
        # lte = f'Неравенства "меньше или равно":\n{str(self.lte_list)}\n'
        # b = f'Вектор правых частей:\n{self.b}\n'
        csp = f'Номера переменных с ограничением неотрицательности (>= 0):\n{str(self.constraints_sgn_plus_list)}\n'
        csm = f'Номера переменных с ограничением неположительности (<= 0):\n{str(self.constraints_sgn_minus_list)}\n'
        result = type_problem + target_func + equals + gte + lte + csp + csm
        return result


        # equals = f'Равенства:\n{str(self.eq_list)}\n'
        # gte = f'Неравенства "больше или равно":\n{str(self.gte_list)}\n'
        # lte = f'Неравенства "меньше или равно":\n{str(self.lte_list)}\n'
        # csp = f'Номера переменных с ограничением неотрицательности:\n{str(self.constraints_sgn_plus_list)}\n'
        # csm = f'Номера переменных с ограничением неположительности:\n{str(self.constraints_sgn_minus_list)}\n'
        # result = type_problem + target_func + equals + gte + lte + csp + csm
        # return result
