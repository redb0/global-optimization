import numpy as np
from typing import Union, List, Tuple
import matplotlib.pyplot as plt

from graph.Graph import Graph


Num = Union[int, float]


class LineGraph(Graph):
    """Класс для построения линейных графиков
    Поля:
        _title      : название графика в виде строки
        _algorithms : список алгоритмов для которых строиться график.
        _param      : параметр по которому, зависимость от которого будет отражена на графике.
        _max_range  : минимальное значение параметра 
        _min_range  : максимальное значение параметра
        _step       : шаг
    """
    # Ограничим возможный атрибуты класса с поомщью __slots__ (они наследуются),
    # как-то можно с помощью nametuple, но я фиг знает как это сделать в классе с методами
    # также если написать например x = [] сразу после класса будет общее поле для всех экземпляров
    __slots__ = ("_title", "_algorithms", "_param", "_max_range", "_min_range", "_step")  # "_type_p"

    def __init__(self, title, alg, param, max_range, min_range, step):
        super().__init__()
        self._title = title
        self._algorithms = alg
        self._param = param
        self._min_range = min_range
        self._max_range = max_range
        self._step = step

    def plot(self):
        # TODO: сделать либо через наследование либо просто методом
        print(self._title)
        print(self._algorithms)
        print(self._min_range)
        print(self._max_range)
        print(self._step)
        # легенда - сверху риссунка, либо отключена.

        x, data = self.make_data()

        plt.subplot()

        for i in range(len(data)):
            # TODO: сделать label для одинаковых алгоритмов
            plt.plot(data[i], label=self._algorithms[i].get_name())

        # bbox_to_anchor - точка к которой закреплена легенда
        # loc - положение относительно точки.
        # 1 - слева, снизу
        # 2 - спара, снизу
        # 3 - справа, сверху
        # 4 - слева, сверху
        # borderaxespad=0. - ширина пространства между границами рисунка и легенды
        # ncol=2, количество столбцов для расположения подписей
        plt.legend(bbox_to_anchor=(0., 1.02), loc=3,
                   ncol=2, borderaxespad=0.)

        plt.show()

    def make_data(self) -> Tuple[np.array, List[List[Union[int, float]]]]:
        """
        Метод генерации данных для графика.
        Производится пуски алгоритмов и расчет оценки вероятности по результатам number_runs прогонов.
        Итерирование идет по выбранному параметру.
        :return: 
        """
        # У x интервал типа (a, b]
        x = np.arange(self.min_range, self.max_range, self.step)
        y = []
        print(x)
        for alg in self._algorithms:
            y1 = []
            for i in range(len(x)):
                alg.set_parameter(self._param.get_abbreviation(), x[i])
                probability = alg.find_probability_estimate([0, 0], 0.5, r"C:\Projects_Python\GlobalOptimization2\examples_tf\func1.json", number_runs=3)
                print(probability)
                y1.append(probability)
            y.append(y1)
        print(y)
        return x, y

    # свойства
    @property
    def title(self) -> str:
        return self.title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def min_range(self) -> Num:
        return self._min_range

    @min_range.setter
    def min_range(self, value: Num) -> None:
        self._min_range = value

    @property
    def max_range(self) -> Num:
        return self._max_range

    @max_range.setter
    def max_range(self, value: Num) -> None:
        self._max_range = value

    @property
    def step(self) -> Num:
        return self._step

    @step.setter
    def step(self, value: Num) -> None:
        self._step = value
