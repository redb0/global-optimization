from PyQt5 import QtWidgets

from gui.wdg.PossibleGraphWidget import PossibleGraphWidget
from gui.wdg.RangeWidget import RangeWidget


class LineGraphWidget(PossibleGraphWidget):
    def __init__(self, line_graph_obj):
        super().__init__()
        self.type_graph = "LINE_GRAPH"

        self.line_graph_obj = line_graph_obj

        self.btn_delete = None
        self.btn_plot = None
        self.range_wdg = None

    def get_widget(self, lower_limit=0, top_limit=1000, step_limit=1):
        w = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout()
        self.btn_delete = QtWidgets.QPushButton()
        self.btn_plot = QtWidgets.QPushButton()
        label = QtWidgets.QLabel()
        grid.addWidget(self.btn_plot, 0, 0)
        grid.addWidget(self.btn_delete, 1, 0)
        grid.addWidget(label, 0, 1)
        p = self.line_graph_obj.get_parameters_obj()
        # for i in range(len(p)):
        #     self.range_wdg = RangeWidget(p[i].get_type(),
        #                                  lower_limit=lower_limit,
        #                                  top_limit=top_limit,
        #                                  step_limit=step_limit)
        #     grid.addWidget(self.range_wdg, 1 + i, 1 + i, 1 + i, 3)

        self.range_wdg = RangeWidget(p[0].get_type(),
                                     lower_limit=lower_limit,
                                     top_limit=top_limit,
                                     step_limit=step_limit)
        grid.addWidget(self.range_wdg, 1, 1, 1, 3)
        # w_range = add_layout_range(self.line_graph_obj.get_type(), min_val, max_val, h)
        # grid.addWidget(self.range_wdg, 1, 1, 1, 3)
        # grid.addWidget(spin_box_2, 1, 2)
        # grid.addWidget(spin_box_3, 1, 3)
        w.setLayout(grid)
        # self.list_graph.addWidget(w)
        self.btn_delete.setText(self.translate("MainWindow", "Удалить"))
        self.btn_plot.setText(self.translate("MainWindow", "Построить"))
        label.setText(self.translate("MainWindow", p[0].get_name()))

        self.btn_delete.clicked.connect(self.delete_graph(w))
        self.btn_plot.clicked.connect(lambda: self.plot())

        return w

    def plot(self):
        range_param = [self.range_wdg.spin_box_1.value(),
                       self.range_wdg.spin_box_2.value(),
                       self.range_wdg.spin_box_3.value()]
        self.line_graph_obj.add_param_range([self.line_graph_obj.get_parameters_obj()[0], range_param])

        print(self.line_graph_obj.get_param_range())
        # print(self.line_graph_obj.get_max_range())
        # print(self.line_graph_obj.get_step())
        print(self.line_graph_obj)
