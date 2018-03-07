from PyQt5 import QtWidgets

from gui.wdg.PossibleGraphWidget import PossibleGraphWidget
from gui.window_choose_params import ParamsWindow


class PointGraphWidget(PossibleGraphWidget):
    def __init__(self, point_graph_obj):
        super().__init__()
        self.type_graph = "POINT_GRAPH"

        self.graph_obj = point_graph_obj

        self.btn_delete = None
        self.btn_plot = None
        self.btn_choose = None
        # self.range_wdg = None

    def get_widget(self, parent=None):
        w = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout()
        self.btn_delete = QtWidgets.QPushButton()
        self.btn_plot = QtWidgets.QPushButton()
        self.btn_choose = QtWidgets.QPushButton()
        p = self.graph_obj.get_parameters_obj()
        self.btn_choose.clicked.connect(self.window_choose_params(p[0], parent=parent))
        label = QtWidgets.QLabel()
        grid.addWidget(self.btn_plot, 0, 0)
        grid.addWidget(self.btn_delete, 1, 0)
        grid.addWidget(label, 0, 1)
        grid.addWidget(self.btn_choose, 1, 1)
        self.btn_delete.setText(self.translate("MainWindow", "Удалить"))
        self.btn_plot.setText(self.translate("MainWindow", "Построить"))
        self.btn_choose.setText(self.translate("MainWindow", "Выбрать значения"))
        label.setText(self.translate("MainWindow", p[0].get_name()))
        self.btn_delete.clicked.connect(self.delete_graph(w))
        # self.btn_plot.clicked.connect(lambda: self.qwe())
        w.setLayout(grid)
        return w

    def window_choose_params(self, parameters, parent=None):
        def f():
            if parent.window_choose is None:
                self.window_choose = ParamsWindow(parameters, parent=parent)
                self.window_choose.show()

        return f
        # TODO: сделать открытие дочернего окна для выбора параметров
