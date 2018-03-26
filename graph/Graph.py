from matplotlib.figure import Figure

from matplotlib import rcParams
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, width=5, height=5, dpi=100, fontsize=14):
        self.set_params(fontsize=fontsize)
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = plt.subplot()

    def set_params(self, fontsize=14):
        # lines.linewidth: 3
        # lines.markersize: 10
        params = {"axes.titlesize": fontsize,
                  "axes.labelsize": fontsize,
                  "xtick.labelsize": fontsize,
                  "ytick.labelsize": fontsize}
        rcParams.update(params)

    def set_labels(self, xlabel="", ylabel="", title="", legend_title=""):
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title, loc='center', y=1.1)
        # plt.subplots_adjust(top=0.85)  # пространство между графиком и краями
        # plt.legend(loc='center left', title=legend_title, bbox_to_anchor=(1, 0.5))

    def plot(self):
        """Метод построения графика"""
        pass

    def make_data(self):
        """Метод генерации данных"""
        pass
