# from abc import ABCMeta, abstractmethod
from matplotlib.figure import Figure

import matplotlib as mpl


class Graph:
    # __metaclass__ = ABCMeta

    # TODO: возможно сделать абстрактным
    # @abstractmethod
    def __init__(self, width=5, height=5, dpi=100):
        # TODO: сделать создание фигуры, установку настроек(размер шрифта, шрифт)
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.subplots(111)

    def set_params(self, fontsize):
        # lines.linewidth: 3
        # lines.markersize: 10
        params = {"axes.titlesize": fontsize,
                  "axes.labelsize": fontsize,
                  "xtick.labelsize": fontsize,
                  "ytick.labelsize": fontsize}
        mpl.rcParams.update(params)

    def plot(self):
        pass

    def make_data(self):
        pass

    # @abstractmethod
    # def get_widget(self):
    #     pass
