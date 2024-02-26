from typing import List


class Vector:
    def __init__(self, elements_list: List):
        self.elems = elements_list
        with open('logs.txt', 'a') as log:
            log.write(f'[INFO]: Создан объект {elements_list} класса Vector\n')

    def __str__(self):
        return f'{self.elems}'

    def __len__(self):
        return len(self.elems)

    def __add__(self, other):
        if len(self.elems) != len(other.elems):
            with open('logs.txt', 'a') as log:
                log.write("[ERROR: class Vector, __add__]: Попытка сложить вектора разной длины.\n")
            raise SystemExit

        result = [x + y for x, y in zip(self.elems, other.elems)]
        return Vector(result)

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            result = [x * other for x in self.elems]
            return Vector(result)

    def __rmul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            result = [x * other for x in self.elems]
            return Vector(result)

    def __getitem__(self, item):
        if isinstance(item, List):
            new_elems = []
            for index in item:
                new_elems.append(self.elems[index])
            return Vector(new_elems)

        elif not isinstance(item, int):
            with open('logs.txt', 'a') as log:
                log.write("[ERROR: class Vector, __getitem__]: Попытка обратиться по нецелочисленному индексу.\n")
            raise SystemExit

        if item < 0:
            with open('logs.txt', 'a') as log:
                log.write("[ERROR: class Vector, __getitem__]: Попытка обратиться по отрицательному индексу\n")
            raise SystemExit

        return self.elems[item]

    def __setitem__(self, key, value):
        if not isinstance(key, int) or key < 0:
            with open('logs.txt', 'a') as log:
                log.write("[ERROR: class Vector, __setitem__]: Попытка обратиться по нецелочисленному или"
                          "отрицательному индексу.\n")
            raise SystemExit

        self.elems[key] = value

    def append(self, elem):
        self.elems.append(elem)
