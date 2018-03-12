import numpy as np
from typing import Union

from graph.Graph import Graph


Num = Union[int, float]


class LineGraph(Graph):
    # Ограничим возможный атрибуты класса с поомщью __slots__ (они наследуются),
    # как-то можно с помощью nametuple, но я фиг знает как это сделать в классе с методами
    # также если написать например x = [] сразу после класса будет общее поле для всех экземпляров
    __slots__ = ["_title", "_algorithms", "_max_range", "_min_range", "_step", "_type_p"]

    def __init__(self, title, alg, max_range, min_range, step, type_p):
        super().__init__()
        self._title = title
        self._algorithms = alg
        self._min_range = min_range
        self._max_range = max_range
        self._step = step
        self._type_p = type_p  # что тут храниться??? хз

    # def get_widget(self):
    #     w = QtWidgets.QWidget()
    #     grid = QtWidgets.QGridLayout()
    #     btn_delete = QtWidgets.QPushButton()
    #     btn_plot = QtWidgets.QPushButton()
    #     label = QtWidgets.QLabel()
    #     w_range = self.add_layout_range(t, min_val, max_val, h)
    #     grid.addWidget(btn_plot, 0, 0)
    #     grid.addWidget(btn_delete, 1, 0)
    #     grid.addWidget(label, 0, 1)
    #     grid.addWidget(w_range, 1, 1, 1, 3)
    #     # grid.addWidget(spin_box_2, 1, 2)
    #     # grid.addWidget(spin_box_3, 1, 3)
    #     w.setLayout(grid)
    #     # self.list_graph.addWidget(w)
    #     btn_delete.setText(self.translate("MainWindow", "Удалить"))
    #     btn_plot.setText(self.translate("MainWindow", "Построить"))
    #     label.setText(self.translate("MainWindow", self.name))
    #
    #     btn_delete.clicked.connect(self.delete_graph(w))
    #
    #     return w

    def plot(self):
        # TODO: сделать либо через наследование либо просто методом
        pass

    def make_data(self):
        # У x интервал типа (a, b]
        x = np.arange(self.min_range, self.max_range, self.step)
        # TODO: сделать в классе алгоритма метод run для запуска алгоритма в отдельном потоке

    # свойства
    @property
    def title(self) -> str:
        return self.title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def type(self):  # добавить возвращаемый тип
        return self._type_p

    @type.setter
    def type(self, value):  # добавить принимаемый тип
        self._type_p = value

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
