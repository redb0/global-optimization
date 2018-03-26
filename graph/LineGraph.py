import numpy as np
from typing import Union, List, Tuple
import matplotlib.pyplot as plt
import os

from Settings import Settings
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
        _settings   : общие настройки, экземпляр класса Settings
    """
    # Ограничим возможный атрибуты класса с поомщью __slots__ (они наследуются),
    # как-то можно с помощью nametuple, но я фиг знает как это сделать в классе с методами
    # также если написать например x = [] сразу после класса будет общее поле для всех экземпляров
    __slots__ = ("_title", "_algorithms", "_param", "_max_range", "_min_range", "_step", "_settings")  # "_type_p"

    def __init__(self, title, alg, param, max_range, min_range, step):
        super().__init__(width=5, height=5, dpi=100, fontsize=14)
        self._title = title
        self._algorithms = alg
        self._param = param
        self._min_range = min_range
        self._max_range = max_range
        self._step = step
        self._settings = Settings()

    def plot(self, print_error=None, file_name="line_graph_1.png"):
        x, data, err = self.make_data()
        if err != "":
            if print_error is not None:
                print_error(err)
                return None
            else:
                return None

        for i in range(len(data)):
            # TODO: сделать label для одинаковых алгоритмов
            self.axes.plot(x, data[i], label=self._algorithms[i].get_name())

        # bbox_to_anchor - точка к которой закреплена легенда
        # loc - положение относительно точки.
        # 1 - слева, снизу
        # 2 - спара, снизу
        # 3 - справа, сверху
        # 4 - слева, сверху
        # borderaxespad=0. - ширина пространства между границами рисунка и легенды
        # ncol=2, количество столбцов для расположения подписей
        title = "Зависимость оценки вороятности от " + self._param.get_name()
        xlabel = "Оценка вероятности"
        ylabel = self._param.get_name()
        self.set_labels(xlabel=xlabel, ylabel=ylabel, title=title, legend_title="")
        if self._settings.legend_position == "top":
            plt.legend(bbox_to_anchor=(0., 1.02), loc=3,
                       ncol=2, borderaxespad=0.)
        # elif self._settings.legend_position == "bottom":
        #     plt.legend(bbox_to_anchor=(0., -0.02), loc=4,
        #                ncol=2, borderaxespad=0.)
        # elif self._settings.legend_position == "left":
        #     plt.legend(bbox_to_anchor=(-0.02, 1.0), loc=4,
        #                ncol=1, borderaxespad=0.)
        elif self._settings.legend_position == "right":
            plt.legend(bbox_to_anchor=(1.02, 1.0), loc=2,
                       ncol=1, borderaxespad=0.)

        plt.savefig(file_name, bbox_inches='tight')
        plt.show()

    def make_data(self) -> Tuple[np.array, List[List[Union[int, float]]], str]:
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
                if os.path.isfile(self._settings.abs_path_test_func):
                    probability = alg.find_probability_estimate(self._settings.real_extrema,
                                                                self._settings.epsilon,
                                                                self._settings.abs_path_test_func,
                                                                number_runs=self._settings.number_of_runs)
                else:
                    return np.array([]), [], "Не выбрана тестовая функция."
                print(probability)
                y1.append(probability)
            y.append(y1)
        print(y)
        return x, y, ""

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
