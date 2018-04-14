from PyQt5 import QtWidgets

from graph.HeatMap import HeatMap
from gui.wdg.PossibleGraphWidget import PossibleGraphWidget
from gui.wdg.RangeWidget import RangeWidget
from gui.wdg.SelectionWidget import SelectionWidget


class HeatMapWidget(PossibleGraphWidget):
    def __init__(self, graph_obj):
        super().__init__()
        self.type_graph = "HEAT_MAP"

        self.graph_obj = graph_obj

        self.selected_value = []
        self.active_window = None

        self.btn_delete = None
        self.btn_plot = None
        self.range_wdg = None

    def get_widget(self, lower_limit=0, top_limit=1000, step_limit=1, algorithm=None, print_error=None):
        w = QtWidgets.QWidget()
        self.grid = QtWidgets.QGridLayout()
        self.btn_delete = QtWidgets.QPushButton()
        self.btn_plot = QtWidgets.QPushButton()
        self.btn_delete.setMaximumWidth(100)
        self.btn_plot.setMaximumWidth(100)
        self.grid.addWidget(self.btn_plot, 0, 0)
        self.grid.addWidget(self.btn_delete, 1, 0)

        p = self.graph_obj.get_parameters_obj()
        for i in range(len(p)):
            if p[i].allowable_values is not None:
                self.range_wdg = SelectionWidget(p[i], parent=self)
            else:
                self.range_wdg = RangeWidget(p[i].get_type(),
                                             lower_limit=lower_limit,
                                             top_limit=top_limit,
                                             step_limit=step_limit)
            self.grid.addWidget(self.range_wdg, i, 1)
        w.setLayout(self.grid)
        self.btn_delete.setText(self.translate("MainWindow", "Удалить"))
        self.btn_plot.setText(self.translate("MainWindow", "Построить"))

        self.btn_delete.clicked.connect(self.delete_graph(w))
        self.btn_plot.clicked.connect(lambda: self.plot(print_error, algorithm))

        return w

    def plot(self, print_error, algorithm):
        axis_range = []
        p = self.graph_obj.get_parameters_obj()
        j = 0
        for i in range(len(p)):
            if p[i].allowable_values is not None:
                axis_range.append(self.selected_value[j])
                j += 1
            else:
                item = self.grid.itemAt(i + 2).widget()
                if type(item) is RangeWidget:
                    down = item.spin_box_1.value()
                    high = item.spin_box_2.value()
                    step = round(item.spin_box_3.value(), 2)
                    if (down >= high) or (step <= 0) or (step >= (high - down)):
                        error = "Параметры итерирования заданы некорректно"
                        print_error(error)
                        print(error)
                    x = down
                    axis = []
                    while x <= high:
                        axis.append(x)
                        x += step
                    axis_range.append(axis)
        heat_map = HeatMap("Тепловая карта", algorithm, self.graph_obj.get_parameters_obj(), axis_range)
        heat_map.plot(print_error=print_error)
