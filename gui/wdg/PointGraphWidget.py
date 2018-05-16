from PyQt5 import QtWidgets

from graph.PointGraph import PointGraph
from gui.wdg.PossibleGraphWidget import PossibleGraphWidget
from gui.window_choose_params import ParamsWindow


class PointGraphWidget(PossibleGraphWidget):
    def __init__(self, point_graph_obj):
        super().__init__()
        self.type_graph = "POINT_GRAPH"

        self.graph_obj = point_graph_obj
        self.selected_value = []

        self.btn_delete = None
        self.btn_plot = None
        self.btn_choose = None

    def get_widget(self, parent=None, print_error=None, algorithms=None):
        w = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout()
        self.btn_delete = QtWidgets.QPushButton()
        self.btn_plot = QtWidgets.QPushButton()
        self.btn_choose = QtWidgets.QPushButton()
        self.btn_delete.setMaximumWidth(100)
        self.btn_plot.setMaximumWidth(100)
        p = self.graph_obj.get_parameters_obj()
        self.btn_choose.clicked.connect(self.window_choose_params(p, parent=parent))
        label = QtWidgets.QLabel()
        grid.addWidget(self.btn_plot, 0, 0)
        grid.addWidget(self.btn_delete, 1, 0)
        grid.addWidget(label, 0, 1)
        grid.addWidget(self.btn_choose, 1, 1)
        self.btn_delete.setText(self.translate("MainWindow", "Удалить"))
        self.btn_plot.setText(self.translate("MainWindow", "Построить"))
        self.btn_choose.setText(self.translate("MainWindow", "Выбрать значения"))
        label.setText(self.translate("MainWindow", p.get_name()))
        self.btn_delete.clicked.connect(self.delete_graph(w))
        self.btn_plot.clicked.connect(lambda: self.plot(print_error, algorithms))
        w.setLayout(grid)
        return w

    def plot(self, print_error, algorithms):
        if not self.selected_value:
            error = "Не выбраны параметры"
            print_error(error)
            print(error)
        else:
            self.graph_obj.add_param_range([self.graph_obj.get_parameters_obj(), self.selected_value])

            line_graph = PointGraph(algorithms, self.graph_obj.get_parameters_obj(), self.selected_value)
            line_graph.plot(print_error=print_error)

    def window_choose_params(self, parameters, parent=None):
        def f():
            if parent.window_choose is None:
                self.window_choose = ParamsWindow(parameters, parent=self)
                self.window_choose.show()

        return f
        # TODO: переделать в pop up
