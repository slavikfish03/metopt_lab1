from DualProblemLP import *

if __name__ == "__main__":
    open('logs.txt', 'w').close()
    # general_problem_lp_primary = GeneralProblemLP()
    # print(general_problem_lp_primary)
    #
    # standart_problem_lp_primary = StandartProblemLP(general_problem_lp_primary)
    #
    # general_problem_lp_dual = DualProblemLP(general_problem_lp_primary)
    # print(general_problem_lp_dual)
    #
    # canonic_problem_lp_primary = CanonicProblemLP(standart_problem_lp_primary)
    # print(canonic_problem_lp_primary)
    #
    # standart_problem_lp_dual = StandartProblemLP(general_problem_lp_dual)
    # canonic_problem_lp_dual = CanonicProblemLP(standart_problem_lp_dual)
    #
    # print(canonic_problem_lp_dual)

    # standart_problem_lp = StandartProblemLP(general_problem_lp)
    # print(standart_problem_lp)
    #
    # canonic_problem_lp = CanonicProblemLP(standart_problem_lp)
    # print(canonic_problem_lp)

    vec1 = Vector([10, 20, 30, 15, 25])
    # vec1[1] = [7, 8]
    # print(vec1)
    vec2 = Vector([5, 70, 50, 80, 100])
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

    vec3 = vec1 + vec2
    # print(vec1)
    print(vec3)
    #
    N = [0, 2, 4]
    print(vec3[N])
    print(vec3)
    #
    # matr1 = Matrix([vec1, vec2, vec3])
