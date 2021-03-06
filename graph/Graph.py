from matplotlib.figure import Figure
from matplotlib import rcParams
import matplotlib.pyplot as plt


class Graph:
    """
    Родительский класс для классов описывающих графики.
    При инициализации создает пустую область для рисования.
    Содержит методы plot и make_data, которые необходимо реализовать в классах наследниках.
    """
    def __init__(self, width=5, height=5, dpi=100, fontsize=14):
        self.set_params(fontsize=fontsize)
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = plt.subplot()
        plt.grid(True)

    def set_params(self, fontsize=14):
        """Метод установки параметров"""
        params = {"axes.titlesize": fontsize,
                  "axes.labelsize": fontsize,
                  "xtick.labelsize": fontsize,
                  "ytick.labelsize": fontsize}
        rcParams.update(params)

    def set_labels(self, xlabel: str ="", ylabel: str ="", title: str ="", legend_title: str ="") -> None:
        """
        Метод нанесения подписей
        :param xlabel       : подпись оси X
        :param ylabel       : подпись оси Y
        :param title        : заголовок графика
        :param legend_title : заголовок легенды
        :return: None
        """
        plt.xlabel(xlabel)
        plt.ylabel(ylabel, rotation=0)
        # if len(ylabel) > 10:
        #     self.axes.yaxis.set_label_coords(-0.1, 0.5)
        # self.axes.yaxis.set_label_coords(-0.05, 1.02)
        # if len(xlabel) > 10:
        #     self.axes.xaxis.set_label_coords(1.1, -0.025)
        # else:
        #     self.axes.xaxis.set_label_coords(1.02, -0.025)
        plt.yticks(rotation=0)
        plt.title(title, loc='center', y=1.1)
        # plt.subplots_adjust(top=0.85)  # пространство между графиком и краями
        # plt.legend(loc='center left', title=legend_title, bbox_to_anchor=(1, 0.5))

    def set_legend_pos(self, position: str ="right") -> None:
        """
        Метод установки позиции легенды.
        :param position: позиция (top, bottom, left, right)
        :return: None
        """
        if position == "top":
            plt.legend(bbox_to_anchor=(0., 1.02), loc=3,
                       ncol=1, borderaxespad=0.)
        # elif self._settings.legend_position == "bottom":
        #     plt.legend(bbox_to_anchor=(0., -0.02), loc=4,
        #                ncol=2, borderaxespad=0.)
        # elif self._settings.legend_position == "left":
        #     plt.legend(bbox_to_anchor=(-0.02, 1.0), loc=4,
        #                ncol=1, borderaxespad=0.)
        elif position == "right":
            plt.legend(bbox_to_anchor=(1.02, 1.0), loc=2,
                       ncol=1, borderaxespad=0.)

    def plot(self):
        """Метод построения графика"""
        pass

    def make_data(self):
        """Метод генерации данных"""
        pass
