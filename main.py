from DualProblemLP import *
from MethodExtremePoints import *
from SimplexMethod import *

if __name__ == "__main__":
    open('logs.txt', 'w').close()


    general_problem_lp_primary = GeneralProblemLP()
    print("\n\n__________\nПРЯМАЯ ЗАДАЧА:\n__________\n\n")
    print(general_problem_lp_primary)

    standart_problem_lp_primary = StandartProblemLP(general_problem_lp_primary)
    #print(standart_problem_lp_primary)

    canonic_problem_lp_primary = CanonicProblemLP(standart_problem_lp_primary)
    #print(canonic_problem_lp_primary)

    print("\n\n__________\nРЕШЕНИЕ ПРЯМОЙ ЗАДАЧИ. МЕТОД ПЕРЕБОРА КРАЙНИХ ТОЧЕК:\n__________\n\n")
    ExtremePointsPrimary = MethodExtremePoints(canonic_problem_lp_primary)
    x_primary, val_primary = ExtremePointsPrimary.solve()
    print("Оптимальный вектор: ")
    print(x_primary[0])
    print("Оптимальное значение целевой функции: ")
    print(val_primary)


    general_problem_lp_dual = DualProblemLP(general_problem_lp_primary)
    print("\n\n__________\nДВОЙСТВЕННАЯ ЗАДАЧА:\n__________\n\n")
    print(general_problem_lp_dual)
    standart_problem_lp_dual = StandartProblemLP(general_problem_lp_dual)
    #print(standart_problem_lp_dual)
    canonic_problem_lp_dual = CanonicProblemLP(standart_problem_lp_dual)
    #print(canonic_problem_lp_dual)

    print("\n\n__________\nРЕШЕНИЕ ДВОЙСТВЕННОЙ ЗАДАЧИ. МЕТОД ПЕРЕБОРА КРАЙНИХ ТОЧЕК:\n__________\n\n")
    ExtremePointsDual = MethodExtremePoints(canonic_problem_lp_dual)
    x_dual, val_dual = ExtremePointsDual.solve()
    print("Оптимальный вектор: ")
    print(x_dual[0])
    print("Оптимальное значение целевой функции: ")
    print(val_dual)

    print("\n\n__________\nПРЯМАЯ ЗАДАЧА:\n__________\n\n")
    print(general_problem_lp_primary)

    print("\n\n__________\nРЕШЕНИЕ ПРЯМОЙ ЗАДАЧИ. ТАБЛИЧНЫЙ СИМПЛЕКС-МЕТОД:\n__________\n\n")
    SimplexMethodPrimary = SimplexMethod(canonic_problem_lp_primary.C, canonic_problem_lp_primary.A,
                                         canonic_problem_lp_primary.b, canonic_problem_lp_primary.changes_dict,
                                         canonic_problem_lp_primary.x_limits_start)
    solution_primary = SimplexMethodPrimary.solve()
    print("Оптимальное значение целевой функции: ")
    print(solution_primary)

    print("\n\n__________\nДВОЙСТВЕННАЯ ЗАДАЧА:\n__________\n\n")
    print(general_problem_lp_dual)

    print("\n\n__________\nРЕШЕНИЕ ДВОЙСТВЕННОЙ ЗАДАЧИ. ТАБЛИЧНЫЙ СИМПЛЕКС-МЕТОД:\n__________\n\n")
    SimplexMethodDual = SimplexMethod(canonic_problem_lp_dual.C, canonic_problem_lp_dual.A,
                                      canonic_problem_lp_dual.b, canonic_problem_lp_dual.changes_dict,
                                      canonic_problem_lp_dual.x_limits_start)
    solution_dual = SimplexMethodDual.solve()
    print("Оптимальное значение целевой функции: ")
    print(solution_dual)


    # vec1 = Vector([10, 20, 30, 15, 25])
    # vec1[1] = [7, 8]
    # print(vec1)
    # vec2 = Vector([5, 70, 50, 80, 100])
    #
    # v1 = Vector([2, 4, 0, 9, 0])
    # v2 = Vector([-2, 1, 3, 89, 11])
    # v3 = Vector([-1, 0, 1, 13, 13])
    # v4 = Vector([90, 12, 74, 5, 2])
    # A = Matrix([v1, v2, v3, v4])
    #
    # print(type(A[1].elems))
    # b = Vector([1, 2, -1, 6, 8])
    #
    # M = [0, 2, 3]
    # N = [0, 3]
    # print(A[M, N])
    # print(b[N])
    #
    # print(A[M, N] * b[N])

    # vec3 = vec1 + vec2
    # # print(vec1)
    # print(vec3)
    # #
    # N = [0, 2, 4]
    # print(vec3[N])
    # print(vec3)
    #
    # matr1 = Matrix([vec1, vec2, vec3])
