import numpy as np

from typing import Tuple

from Vector import *


class Matrix:
    def __init__(self, rows: List):
        self.rows = rows
        with open('logs.txt', 'a') as log:
            log.write(f'[INFO]: Создан объект {[str(vec) for vec in self.rows]} класса Matrix.\n')

    def __str__(self):
        string = "(\n"
        for row in self.rows:
            string += f"{row},\n"
        string += ")"
        return string

    def __len__(self):
        return len(self.rows)

    def __mul__(self, other):
        if isinstance(other, Vector):
            if len(self.rows[0]) != len(other):
                with open('logs.txt', 'a') as log:
                    log.write("[ERROR: class Matrix, __mul__]: Несоответствие размеров при умножении матрицы на вектор.\n")
                raise SystemExit
            new_elems = []
            for row in self.rows:
                elem = 0
                for i in range(len(other)):
                    elem = elem + row[i] * other[i]
                new_elems.append(elem)
            return Vector(new_elems)

    def __getitem__(self, indexes_list):
        # [ [], [] ]
        print(type(indexes_list))
        if isinstance(indexes_list, int) or isinstance(indexes_list, float):
            if not isinstance(indexes_list, int):
                with open('logs.txt', 'a') as log:
                    log.write("[ERROR: class Matrix, __getitem__]: Попытка обратиться по нецелочисленному индексу.\n")
                raise SystemExit
            if indexes_list < 0:
                with open('logs.txt', 'a') as log:
                    log.write("[ERROR: class Matrix, __getitem__]: Попытка обратиться по отрицательному индексу.\n")
                raise SystemExit
            return self.rows[indexes_list]
        if isinstance(indexes_list, List):
            if len(indexes_list) != 1:
                new_elems = []
                for index in indexes_list:
                    new_elems.append(self.rows[index])
                return Matrix(new_elems)

        elif isinstance(indexes_list, Tuple):
            M = indexes_list[0]
            N = indexes_list[1]

            new_rows = []
            for index_row in M:
                new_rows.append(self.rows[index_row])

            # List(Vector)

            new_elems = []
            for elem in new_rows:
                new_elems.append(elem[N])

            return Matrix(new_elems)

    def __add__(self, other):
        rows = self.rows.copy()
        for i in range(len(rows)):
            rows[i].append(other[i])
        return Matrix(rows)

    def transpose(self):
        count_new_rows = len(self.rows[0])

        new_b_list = []
        for i in range(count_new_rows):
            new_b_elem = [row[i] for row in self.rows]
            new_b_list.append(new_b_elem)

        return Matrix(new_b_list)

    def copy(self):
        new_rows = []
        for row in self.rows:
            new_rows.append(row.copy())

        return Matrix(new_rows)

    def convert_to_np(self):
        m_list = []
        for vec in self.rows:
            m_list.append(vec.elems)
        return np.array(m_list)

    def rang(self):
        matrix = self.convert_to_np()
        return np.linalg.matrix_rank(matrix)

    def det(self):
        matrix = self.convert_to_np()
        return np.linalg.det(matrix)
