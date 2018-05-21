import os

import numpy as np

from Settings import Settings
from graph.Graph import Graph

import matplotlib.pyplot as plt

from support_func import generate_rand_int_list, make_report


class PointGraph(Graph):
    """Класс для построения точечного графика"""
    def __init__(self, alg, param, selected_value):
        super().__init__()
        self._algorithms = alg
        self._settings = Settings()
        self._param = param
        self.selected_value = selected_value

    def plot(self, print_error=None, file_name="point_graph_1.png"):
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
                           linewidth=1.5, linestyle='', marker=markers_list[markers_idx[i]])

        title = "Зависимость оценки вороятности от " + self._param.get_name()
        xlabel = self._param.label_TeX
        ylabel = "$\widehat {P}{_\delta}$   "  # "Оценка вероятности"
        self.set_labels(xlabel=xlabel, ylabel=ylabel, title=title, legend_title="")
        self.set_legend_pos(self._settings.legend_position)

        plt.savefig(file_name, bbox_inches='tight')
        plt.show()

    def make_data(self):
        x = np.array(self.selected_value[0])
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
                print(probability)
                y1.append(probability)
            alg.set_parameter(x_name, stock_value)
            y.append(y1)
        return x, y, ""
