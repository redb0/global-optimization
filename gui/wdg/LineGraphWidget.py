from PyQt5 import QtWidgets

from gui.wdg.PossibleGraphWidget import PossibleGraphWidget
from gui.wdg.RangeWidget import RangeWidget
from graph import LineGraph


class LineGraphWidget(PossibleGraphWidget):
    def __init__(self, line_graph_obj):
        super().__init__()
        self.type_graph = "LINE_GRAPH"

        self.line_graph_obj = line_graph_obj

        self.btn_delete = None
        self.btn_plot = None
        self.range_wdg = None

    def get_widget(self, lower_limit=0, top_limit=1000, step_limit=1, algorithms=None, print_error=None):
        w = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout()
        self.btn_delete = QtWidgets.QPushButton()
        self.btn_plot = QtWidgets.QPushButton()
        self.btn_delete.setMaximumWidth(100)
        self.btn_plot.setMaximumWidth(100)
        label = QtWidgets.QLabel()
        grid.addWidget(self.btn_plot, 0, 0)
        grid.addWidget(self.btn_delete, 1, 0)
        grid.addWidget(label, 0, 1)
        p = self.line_graph_obj.get_parameters_obj()

        self.range_wdg = RangeWidget(p.get_type(),
                                     lower_limit=lower_limit,
                                     top_limit=top_limit,
                                     step_limit=step_limit)
        grid.addWidget(self.range_wdg, 1, 1, 1, 3)
        w.setLayout(grid)
        self.btn_delete.setText(self.translate("MainWindow", "Удалить"))
        self.btn_plot.setText(self.translate("MainWindow", "Построить"))
        label.setText(self.translate("MainWindow", p.get_name()))

        self.btn_delete.clicked.connect(self.delete_graph(w))
        self.btn_plot.clicked.connect(lambda: self.plot(print_error, algorithms))
        return w

    def plot(self, print_error, algorithms):
        down = self.range_wdg.spin_box_1.value()
        high = self.range_wdg.spin_box_2.value()
        step = round(self.range_wdg.spin_box_3.value(), 2)
        if (down >= high) or (step <= 0) or (step >= (high - down)):
            error = "Параметры итерирования заданы некорректно"
            print_error(error)
            print(error)
        else:
            range_param = [down, high, step]
            self.line_graph_obj.add_param_range([self.line_graph_obj.get_parameters_obj(), range_param])

            line_graph = LineGraph.LineGraph("title", algorithms, self.line_graph_obj.get_parameters_obj(),
                                             high, down, step)
            line_graph.plot(print_error=print_error)
