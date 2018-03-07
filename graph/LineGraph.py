from PyQt5 import QtWidgets

from graph.Graph import Graph


class LineGraph(Graph):
    def __init__(self, name_param, alg, max_range, min_range, step, type_p):
        super().__init__()
        self.name = name_param
        self.algorithms = alg
        self.min_range = min_range
        self.max_range = max_range
        self.step = step
        self.type_p = type_p

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

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type_p

    def set_min_range_value(self, value):
        self.min_range = value

    def set_max_range_value(self, value):
        self.max_range = value

    def set_step_value(self, value):
        self.step = value

    def get_min_range(self):
        return self.min_range

    def get_max_range(self):
        return self.max_range

    def get_step(self):
        return self.step
