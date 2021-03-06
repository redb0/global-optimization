import json
import os
from typing import Union, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

from Settings import Settings
from graph.Graph import Graph
from support_func import generate_rand_int_list, get_delta, make_report

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
    # Ограничим возможный атрибуты класса с поомщью __slots__ (они наследуются)
    __slots__ = ("_title", "_algorithms", "_param", "_max_range", "_min_range", "_step", "_settings")

    def __init__(self, title, alg, param, max_range, min_range, step):
        super().__init__(width=5, height=6, dpi=100, fontsize=12)
        self._title = title
        self._algorithms = alg
        self._param = param
        self._min_range = min_range
        self._max_range = max_range
        self._step = step
        self._settings = Settings()

    def plot(self, print_error=None, file_name="line_graph_1.png"):
        """
        Метод построения и вывода линейного графика.
        :param print_error : функция обработки ошибки, принимающая строку.
        :param file_name   : имя файла для сохранения файла в виде строки.
        :return: None.
        """
        markers = ['o', 'x', 'v', '^', '<',
                   '>', 's', 'p', '*', 'h',
                   'H', '+', 'D', 'd', '|', '_']
        x, data, err = self.make_data()
        if err != "":
            if print_error is not None:
                print_error(err)
                return None
            else:
                return None

        if len(data) > len(markers):
            markers_list = markers.append(markers[:(len(data) - len(markers))])
        else:
            markers_list = markers
        markers_idx = generate_rand_int_list(len(data))

        for i in range(len(data)):
            self.axes.plot(x, data[i], label=self._algorithms[i].get_identifier_name(),
                           linewidth=1.5, marker=markers_list[markers_idx[i]])

        # bbox_to_anchor - точка к которой закреплена легенда
        # loc - положение относительно точки.
        # 1 - слева, снизу
        # 2 - спара, снизу
        # 3 - справа, сверху
        # 4 - слева, сверху
        # borderaxespad=0. - ширина пространства между границами рисунка и легенды
        # ncol=2, количество столбцов для расположения подписей
        title = "Зависимость оценки вороятности от " + self._param.get_name()
        xlabel = self._param.label_TeX
        ylabel = "$\widehat {P}{_\delta}$   "  # "Оценка вероятности"
        self.set_labels(xlabel=xlabel, ylabel=ylabel, title=title, legend_title="")
        self.set_legend_pos(self._settings.legend_position)

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
        x_name = self._param.get_abbreviation()
        y = []
        for alg in self._algorithms:
            y1 = []
            stock_value = alg.get_value_param_on_abbreviation(x_name)
            for i in range(len(x)):
                alg.set_parameter(x_name, x[i])
                if os.path.isfile(self._settings.abs_path_test_func):
                    probability, data = alg.find_probability_estimate(self._settings.epsilon,
                                                                      self._settings.abs_path_test_func,
                                                                      number_runs=self._settings.number_of_runs)
                    if self._settings.report:
                        make_report(data, "report_" + alg.get_identifier_name() + '.json')
                else:
                    return np.array([]), [], "Не выбрана тестовая функция."
                y1.append(probability)
            alg.set_parameter(x_name, stock_value)
            y.append(y1)
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


# TODO: Переделать в классы.
# для графика сходимости по значениям функции
# для графика дисперсии
def line_graph(data, x, lbl=None, file_name="", x_label="", y_label="", title="", marker=None):
    # TODO: Добавить документацию
    graph = Graph()
    graph.set_params()
    settings = Settings()
    markers = ['o', 'x', 'v', '^', '<',
               '>', 's', 'p', '*', 'h',
               'H', '+', 'D', 'd', '|', '_']

    graph.set_labels(xlabel=x_label, ylabel=y_label, title=title, legend_title="")

    if len(data) > len(markers):
        markers_list = markers.append(markers[:(len(data) - len(markers))])
    else:
        markers_list = markers
    markers_idx = generate_rand_int_list(len(data))
    data = np.array(data)
    if len(data.shape) == 1:
        graph.axes.plot(x, data, label=lbl, linewidth=1.5, marker=markers[0] if marker is None else marker)
    else:
        for i in range(len(data)):
            graph.axes.plot(x, data[i], label=lbl[i], linewidth=1.5,
                            marker=markers_list[markers_idx[i]] if marker is None else marker)
    graph.set_legend_pos(settings.legend_position)
    plt.savefig(file_name, bbox_inches='tight')
    plt.show()


def graph_convergence_coord(data, x, lbl=None, file_name=None, x_label="", y_label="", title="", single_graph=False, marker=None):
    """
    Функция построения графика сходимости по координатам.
    Строит график изменения координат в зависимости от итераций.
    Пример вызова 1:
        x = [0, 1, 2, 3, 4, 5]  # номер итерации
        data = [[5, 5], [2.43, 4.7], [1.52, 4.61], [0.5, 4.56], [-1.1, 4.2], [-1.99, 4.01]]  # изменения координат
        labels = ["${x}{_0}$", "${x}{_1}$"]  # массив подписей к данным с использованием нотации TeX.
        graph_convergence_coord(data, x, lbl=labels, 
                                file_name="42.png", x_label="t", y_label="x", 
                                title="Сходимость алгоритма к глобальному экстремуму по координатам", 
                                single_graph=False)
    Пример вызова 2:
        x = [0, 1, 2, 3, 4, 5]  # номер итерации
        data = [[[5, 5], [2.43, 4.7], [1.52, 4.61], [0.5, 4.56], [-1.1, 4.2], [-1.99, 4.01]],
                [[5, 5], [2.5, 4.89], [1.38, 4.64], [-0.12, 4.27], [-1.76, 4.15], [-2.03, 3.98]]]
        labels = [["${x}{_0} GSA$", "${x}{_1} GSA$"], 
                  ["${x}{_0} SAC$", "${x}{_1} SAC$"]]
        graph_convergence_coord(data, x, lbl=labels, 
                                file_name="42.png", x_label="t", y_label="x", 
                                title="Сходимость алгоритма к глобальному экстремуму по координатам", 
                                single_graph=False)
    Если в последнем примере single_graph=False, то будет два графика отдельно для GSA и для SAC 
    (имена файлов в этом случае будут "42_0.png" и "42_1.png").
    Если же single_graph=True, то будет один график с 4-мя линиями.
    
    :param data         : список с данными.
    :param x            : одномерный список значений для рисок по оси X.
    :param lbl          : список подписей для линий.
    :param file_name    : название файла для сохранения графика, например : "42.png".
    :param x_label      : подпись оси X, в виде строки. 
    :param y_label      : подпись оси Y, в виде строки.
    :param title        : название графика.
    :param single_graph : флаг, если установлено False - график сходимоти для каждого набора будет свой,
                          если установлено значение True - все данные будут на одном графике.
    :return: None
    """
    graph = Graph()
    graph.set_params()
    settings = Settings()
    dim = settings.dimension
    markers = ['o', 'x', 'v', '^', '<',
               '>', 's', 'p', '*', 'h',
               'H', '+', 'D', 'd', '|', '_']

    graph.set_labels(xlabel=x_label, ylabel=y_label, title=title, legend_title="")

    data = np.array([np.array(d) for d in data])

    if 2 * len(data) > len(markers):
        markers_list = markers.append(markers[:(2 * len(data) - len(markers))])
    else:
        markers_list = markers
    markers_idx = generate_rand_int_list(2 * len(data))
    if len(data.shape) == 2 and data.shape[-1] == dim:
        if len(lbl) != dim:
            raise ValueError("Ожидается параметр lbl длиной " + str(dim) +
                             ", текущая длина " + str(len(lbl)))
        marker = '' if (marker is None) and (len(data) >= 15) else None
        for j in range(dim):
            graph.axes.plot(x, data[:, j], label=lbl[0][j], linewidth=1.5, marker=markers_list[markers_idx[j]] if marker is None else marker)
    elif len(data.shape) == 2 and data.shape[-1] != dim:
        marker = '' if (marker is None) and (data.shape[-1] >= 15) else None
        for j in range(len(data)):
            graph.axes.plot(x, data[j], label=lbl[j], linewidth=1.5, marker=markers_list[markers_idx[j]] if marker is None else marker)
    else:
        lbl = np.array(lbl)
        if lbl.shape[0] != len(data) or lbl.shape[-1] != dim:
            raise ValueError("Ожидается параметр lbl длиной " + str(len(data)) +
                             ", текущая длина " + str(len(lbl)) +
                             ", с подмассивами длиной " + str(dim) +
                             ", текущая длина подмассивов" + str(lbl.shape[-1]))
        marker = '' if (marker is None) and (data.shape[-2] >= 15) else None
        for i in range(len(data)):
            for j in range(dim):
                graph.axes.plot(x, data[i, :, j], label=lbl[i][j], linewidth=1.5,
                                marker=markers_list[markers_idx[dim*i+j]] if marker is None else marker)
            if not single_graph:
                graph.set_legend_pos(settings.legend_position)
                # name = file_name[:file_name.find('.')] + "_" + str(i) + file_name[file_name.find('.'):]
                plt.savefig(file_name[i], bbox_inches='tight')
                plt.show()
                if i == len(data) - 1:
                    return
                else:
                    graph = Graph()
                    graph.set_labels(xlabel=x_label, ylabel=y_label, title=title, legend_title="")

    graph.set_legend_pos(settings.legend_position)
    plt.savefig(file_name, bbox_inches='tight')
    plt.show()


def motion_point_graph(data, func, lbl=None, file_name="", x_label="", y_label="", title=""):
    """
    Функция построения графика движения точки.
    На фоне располагается график изолиний тестовой функции.
    Положение зонда(точки) изображается красными точками на графике.
    Каждое положение соединяется стрелкой со следующим с указанием направления перемещения точки.
    :param data      : координаты точек.
    :param func      : тестовая функция, в виде вызываемого объекта.
    :param lbl       : подпись для точек.
    :param file_name : название файла для сохранения графика.
    :param x_label   : подпись оси X.
    :param y_label   : подпись оси Y.
    :param title     : название графика.
    :return: None
    """
    h = 0.2
    delta = 0.5
    l = 2
    data = np.array(data)
    graph = Graph()
    settings = Settings()
    if settings.dimension != 2:
        raise ValueError("График движения точки строиться для функции двух переменных.")
    with open(settings.abs_path_test_func, 'r') as f:
        tf = json.load(f)
    constraints_x = [tf['constraints_down'][0], tf['constraints_high'][0]]
    constraints_y = [tf['constraints_down'][1], tf['constraints_high'][1]]
    x, y, z, levels = make_contour_data(func, constraints_x, constraints_y, h, delta, l)
    plt.contour(x, y, z, levels=levels)

    arrowprops = {
        'arrowstyle': '-|>',
        'linewidth': 1.5,
        'fc': 'k',  # заливка
        'ec': 'k',  # контур
    }

    for i in range(len(data)):
        graph.axes.plot(data[i][:, 0], data[i][:, 1], label=lbl[i], marker='o', linestyle='')  # color='r'
        for j in range(len(data[i]) - 1):
            graph.axes.annotate('', xy=(data[i][j+1][0], data[i][j+1][1]), xytext=(data[i][j][0], data[i][j][1]),
                                arrowprops=arrowprops)

    graph.axes.grid()
    graph.set_labels(xlabel=x_label, ylabel=y_label, title=title, legend_title="")
    graph.set_legend_pos(settings.legend_position)
    plt.savefig(file_name, bbox_inches='tight')
    plt.show()


def make_contour_data(func, constraints_x, constraints_y, h, delta, l):
    """
    Метод генерации данных для построения графика изолиний.
    :param func          : функция, изолинии которой будут строиться, в виде вызываемого объекта.
    :param constraints_x : ограничения по оси X.
    :param constraints_y : ограничения по оси Y.
    :param h             : шаг сетки.
    :param delta         : переменная для расчета уровней изолиний.
    :param l             : переменная для расчета уровней изолиний.
    :return: xgrid  -
             ygrid  - 
             zgrid  - 
             levels - уровни изолиний.
    """
    x = np.arange(constraints_x[0], constraints_x[1], h)
    y = np.arange(constraints_y[0], constraints_y[1], h)
    xgrid, ygrid = np.meshgrid(x, y)

    zgrid = np.zeros(xgrid.shape)

    for i in range(xgrid.shape[0]):
        for j in range(xgrid.shape[1]):
            zgrid[i][j] = func([xgrid[i][j], ygrid[i][j]])

    levels = []
    for i in get_delta(np.min(zgrid), np.max(zgrid), delta=delta, l=l):
        levels.append(i)

    return xgrid, ygrid, zgrid, levels
