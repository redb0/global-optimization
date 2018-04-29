import os

import seaborn as sns
import matplotlib.pyplot as plt

from Settings import Settings
from graph.Graph import Graph
from support_func import combinations


class HeatMap(Graph):
    def __init__(self, title, alg, param, axis_range):
        super().__init__(width=5, height=6, dpi=100, fontsize=12)
        self._title = title
        self._algorithms = alg[0]
        self._param = param
        self.axis_range = axis_range
        self._settings = Settings()

    def plot(self, print_error=None, file_name="heat_map_1.png"):
        data, er = self.make_data()
        print(self.axis_range)
        if er != "":
            print_error(er)
            return

        print(data)
        ax = sns.heatmap(data, cmap=plt.cm.Blues, linewidths=.1)  # cbar_kws={'label': '$\widehat {P}{_\delta}$'}

        # plt.rc('text', usetex=True)

        cbar_axes = ax.figure.axes[-1]
        cbar_axes.set_ylabel('$\\uparrow$\n  $\widehat{P}{_\delta}$', rotation=0, size=12)

        ax.set_xticklabels(self.axis_range[1], minor=False)
        ax.set_yticklabels(self.axis_range[0], minor=False)

        print(self.axis_range[1][-1], self.axis_range[0][-1])

        plt.xlabel(self._param[1].label_TeX)  # rightarrow
        plt.ylabel(self._param[0].label_TeX, rotation=0)
        if len(self._param[0].label_TeX) > 10:
            self.axes.yaxis.set_label_coords(-0.2, 0.5)
        plt.title(self._title, loc='center', y=1.1)
        plt.yticks(rotation=0)

        # ax.set_xlabel(self._param[0].label_TeX)
        # ax.set_ylabel(self._param[1].label_TeX)

        # self.set_labels(xlabel=self._param[0].label_TeX,
        #                 ylabel=self._param[1].label_TeX,
        #                 title=self._title, legend_title="")

        ax.invert_yaxis()
        plt.arrow(0, 0, len(self.axis_range[1]), 0, width=.0007, color="k", clip_on=False, head_width=0.05,
                  head_length=0.1)
        plt.arrow(0, 0, 0, len(self.axis_range[0]), width=.0007, color="k", clip_on=False, head_width=0.05,
                  head_length=0.1)

        plt.savefig(file_name, bbox_inches='tight')
        plt.show()

    def make_data(self):
        names = []
        stock_values = []
        data = []
        for i in range(len(self._param)):
            names.append(self._param[i].get_abbreviation())
            stock_values.append(self._algorithms.get_value_param_on_abbreviation(names[i]))

        if not os.path.isfile(self._settings.abs_path_test_func):
            return None, "Не выбрана тестовая функция."

        probability = []
        for c in combinations(self.axis_range):
            for j in range(len(c)):
                self._algorithms.set_parameter(names[j], c[j])
            p = self._algorithms.find_probability_estimate(self._settings.epsilon,
                                                           self._settings.abs_path_test_func,
                                                           number_runs=self._settings.number_of_runs)
            probability.append(p)
            if c[-1] == self.axis_range[-1][-1]:
                data.append(probability)
                probability = []
        for i in range(len(stock_values)):
            self._algorithms.set_parameter(names[i], stock_values[i])

        return data, ""
