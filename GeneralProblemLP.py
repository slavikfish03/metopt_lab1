from Matrix import *


class GeneralProblemLP:
    def __init__(self, problem_lp=None):
        if not problem_lp:
            print("Введите количество переменных.\n ВВОД: ")
            n = int(input())
            N = [i for i in range(n)]
            self.N = N

            print(
                "_____\nВведите коэффициенты вектора C (коэффициенты целевой функции) через пробел без лишних "
                "символов.\n "
                "ВВОД: ")
            C_coeffs = str(input())
            C_list = [float(x) for x in C_coeffs.split()]

            if len(C_list) != n:
                with open('logs.txt', 'a') as log:
                    log.write(
                        "[ERROR: input C]: Несоответствие введенных параметров вектора коэффициентов целевой функции.\n")
                raise SystemExit

            print("_____\nВведите 'min', если Вы хотите минимизировать целевую функцию, 'max' -- если "
                  "максимизировать.\n "
                  "ВВОД: ")
            target = str(input())
            if target != 'min' and target != 'max':
                with open('logs.txt', 'a') as log:
                    log.write("[ERROR: input]: Некорректно введена цель задачи (min или max).\n")
                raise SystemExit

            self.target = target
            C = Vector(C_list)
            self.C = C

            print(
                "_____\nВведите 1, если в Вашей задаче есть ограничения-равенства. В противном случае введите 0.\n "
                "ВВОД: ")
            eq_list = []
            is_equals = int(input())
            if is_equals:
                print("_____\nВведите количество равенств.\n ВВОД: ")
                eq_num = int(input())
                print("_____\nВведите равенства в следующем виде: через пробел, последовательно.\n"
                      " Если переменной нет, введите ее коэффициент как 0. В конце последовательности укажите\n"
                      " число, стоящее в правой части.\n"
                      "ПРИМЕР: 3 * x_1 + 7 * x_3 = -6 вводится как '3 0 7 -6', если в задаче три переменные.\n ВВОД: ")
                for _ in range(eq_num):
                    eq_str = str(input())
                    eq_elem = [float(x) for x in eq_str.split()]
                    eq_list.append(eq_elem)
                if eq_num != len(eq_list):
                    with open('logs.txt', 'a') as log:
                        log.write("[ERROR: input]: Несоответствие введеных параметров ограничений-равенств.\n")
                    raise SystemExit
            self.eq_list = eq_list

            print(
                "_____\nВведите 1, если в Вашей задаче есть ограничения-неравенства. В противном случае введите 0.\n "
                "ВВОД: ")
            gte_list = []
            lte_list = []
            is_inequals = int(input())
            if is_inequals:
                print("_____\nВведите количество неравенств со знаком БОЛЬШЕ ЛИБО РАВНО.\n"
                      "Если их нет, введите 0.\n ВВОД: ")
                gte_num = int(input())
                if gte_num != 0:
                    print("_____\nВведите неравенства со знаком БОЛЬШЕ ЛИБО РАВНО в следующем виде: через пробел,\n "
                          "последовательно. Если переменной нет, введите ее коэффициент как 0. В конце\n "
                          "последовательности также через пробел укажите число, стоящее в правой части.\n"
                          ""
                          "ПРИМЕР: 3 * x_1 + 7 * x_3 >= -6 вводится как '3 0 7 -6', если в задаче три переменные.\n "
                          "ВВОД: ")
                    for _ in range(gte_num):
                        gte_str = str(input())
                        gte_elem = [float(x) for x in gte_str.split()]
                        gte_list.append(gte_elem)
                if gte_num != len(gte_list):
                    with open('logs.txt', 'a') as log:
                        log.write("[ERROR: input]: Несоответствие введеных параметров ограничений-неравенств типа "
                                  "'>='.\n")
                    raise SystemExit

                print("_____\nВведите количество неравенств со знаком МЕНЬШЕ ЛИБО РАВНО.\n"
                      "Если их нет, введите 0.\n ВВОД: ")
                lte_num = int(input())
                if lte_num != 0:
                    print("_____\nВведите неравенства со знаком МЕНЬШЕ ЛИБО РАВНО в следующем виде: через пробел,\n "
                          "последовательно. Если переменной нет, введите ее коэффициент как 0. В конце\n "
                          "последовательности также через пробел укажите число, стоящее в правой части.\n"
                          ""
                          "ПРИМЕР: 3 * x_1 + 7 * x_3 <= -6 вводится как '3 0 7 -6', если в задаче три переменные.\n "
                          "ВВОД: ")
                    for _ in range(lte_num):
                        lte_str = str(input())
                        lte_elem = [float(x) for x in lte_str.split()]
                        lte_list.append(lte_elem)
                if lte_num != len(lte_list):
                    with open('logs.txt', 'a') as log:
                        log.write("[ERROR: input]: Несоответствие введеных параметров ограничений-неравенств типа "
                                  "'<='.\n")
                    raise SystemExit

            self.gte_list = gte_list
            self.lte_list = lte_list

            print("_____\nВведите количество ограничений НЕОТРИЦАТЕЛЬНОСТИ на знак для переменных.\n"
                  " Если ограничений нет, введите 0.\n"
                  "ВВОД: ")
            constraints_sgn_plus_num = int(input())
            constraints_sgn_plus_list = []
            if constraints_sgn_plus_num != 0:
                print(
                    "_____\nВведите номера переменных через пробел, имеющих ограничение НЕОТРИЦАТЕЛЬНОСТИ на знак.\n "
                    "ВВОД: ")
                constraints_sgn_plus_str = str(input())
                constraints_sgn_plus_list = [int(x) - 1 for x in constraints_sgn_plus_str.split()]

                if constraints_sgn_plus_num != len(constraints_sgn_plus_list):
                    with open('logs.txt', 'a') as log:
                        log.write("[ERROR: input]: Несоответствие введеных параметров ограничений на знак.\n")
                    raise SystemExit

            self.constraints_sgn_plus_list = constraints_sgn_plus_list

            print("_____\nВведите количество ограничений НЕПОЛОЖИТЕЛЬНОСТИ на знак для переменных.\n"
                  " Если ограничений нет, введите 0.\n"
                  "ВВОД: ")
            constraints_sgn_minus_num = int(input())
            constraints_sgn_minus_list = []
            if constraints_sgn_minus_num != 0:
                print(
                    "_____\nВведите номера переменных через пробел, имеющих ограничение НЕПОЛОЖИТЕЛЬНОСТИ на знак.\n "
                    "ВВОД: ")
                constraints_sgn_minus_str = str(input())
                constraints_sgn_minus_list = [int(x) - 1 for x in constraints_sgn_minus_str.split()]

                if constraints_sgn_minus_num != len(constraints_sgn_minus_list):
                    with open('logs.txt', 'a') as log:
                        log.write("[ERROR: input]: Несоответствие введеных параметров ограничений на знак.\n")
                    raise SystemExit

            self.constraints_sgn_minus_list = constraints_sgn_minus_list

            constraints_sgn_list = constraints_sgn_plus_list + constraints_sgn_minus_list
            if len(set(constraints_sgn_list)) != len(constraints_sgn_list):
                with open('logs.txt', 'a') as log:
                    log.write("[ERROR: input]: На одну и ту же переменную наложены ограничения неотрицательности и "
                              "неположительности.\n")
                raise SystemExit

            self.x_limits_start = []
            for i in range(len(self.N)):
                if self.N[i] in self.constraints_sgn_plus_list:
                    self.x_limits_start.append(1)
                elif self.N[i] in self.constraints_sgn_minus_list:
                    self.x_limits_start.append(-1)
                else:
                    self.x_limits_start.append(0)
        else:
            self.N = problem_lp.N
            self.target = problem_lp.target
            self.C = problem_lp.C
            self.eq_list = problem_lp.eq_list
            self.gte_list = problem_lp.gte_list
            self.lte_list = problem_lp.lte_list
            self.constraints_sgn_plus_list = problem_lp.constraints_sgn_plus_list
            self.constraints_sgn_minus_list = problem_lp.constraints_sgn_minus_list
            self.x_limits_start = problem_lp.x_limits_start

    def __str__(self):
        def sgn(x):
            if x >= 0:
                return '+'
            return '-'

        type_problem = 'Общая задача ЛП:\n'
        target_func = ''
        for i in range(len(self.C) - 1):
            target_func += f' {sgn(self.C[i])} {abs(self.C[i])} * x_{i} '
        target_func += f'{sgn(self.C[len(self.C) - 1])} {abs(self.C[len(self.C) - 1])} * x_{len(self.C) - 1}'
        target_func += f' -> {self.target}\n\n'

        # equals = f'Равенства:\n{str(self.eq_list)}\n'
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
