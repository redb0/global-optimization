from PyQt5 import QtWidgets

from gui.window_choose_params import ParamsWindow
from support_func import get_max_step


class RangeWidget(QtWidgets.QWidget):
    def __init__(self, t, lower_limit=0, top_limit=2000, step_limit=1):
        super().__init__()
        self.type_p = t
        self.lower_limit = lower_limit
        self.top_limit = top_limit
        self.step_limit = step_limit

        # self.min_val = 0
        # self.max_val = 0
        # self.step = 0

        self.spin_box_1 = None
        self.spin_box_2 = None
        self.spin_box_3 = None

        self.setup_ui()

    def setup_ui(self):
        grid = QtWidgets.QGridLayout()
        # w = QtWidgets.QWidget()
        # w.setLayout(grid)
        self.setLayout(grid)
        if self.type_p == int:
            self.spin_box_1 = QtWidgets.QSpinBox()
            # spin_box_1.setMinimum(self.lower_limit)
            # spin_box_1.setMaximum(self.top_limit)
            self.spin_box_2 = QtWidgets.QSpinBox()
            # spin_box_1.valueChanged.connect(spin_box_2.setMinimum)
            # spin_box_2.setMaximum(self.lower_limit)
            self.spin_box_3 = QtWidgets.QSpinBox()
            self.spin_box_3.setSingleStep(self.step_limit)
            # spin_box_3.setMinimum(0)
            # spin_box_1.valueChanged.connect(get_max_step(spin_box_2, spin_box_3))
            # spin_box_2.valueChanged.connect(get_max_step(spin_box_1, spin_box_3))
            # spin_box_3.setSingleStep(self.step_limit)
        if self.type_p == float:
            self.spin_box_1 = QtWidgets.QDoubleSpinBox()
            # spin_box_1.setMinimum(self.lower_limit)
            # spin_box_1.setMaximum(self.top_limit)
            self.spin_box_2 = QtWidgets.QDoubleSpinBox()
            # spin_box_1.valueChanged.connect(spin_box_2.setMinimum)
            # spin_box_2.setMaximum(self.top_limit)
            self.spin_box_3 = QtWidgets.QDoubleSpinBox()
            self.spin_box_3.setSingleStep(0.1)
            # spin_box_1.valueChanged.connect(get_max_step(spin_box_2, spin_box_3))
            # spin_box_2.valueChanged.connect(get_max_step(spin_box_1, spin_box_3))
            # spin_box_3.setSingleStep(self.step_limit)

        self.spin_box_1.setMinimum(self.lower_limit)
        self.spin_box_1.setMaximum(self.top_limit)
        self.spin_box_2.setMaximum(self.top_limit)
        self.spin_box_3.setMinimum(0)

        self.spin_box_1.valueChanged.connect(self.spin_box_2.setMinimum)
        self.spin_box_1.valueChanged.connect(get_max_step(self.spin_box_2, self.spin_box_3))
        self.spin_box_2.valueChanged.connect(get_max_step(self.spin_box_1, self.spin_box_3))

        grid.addWidget(self.spin_box_1, 0, 1)
        grid.addWidget(self.spin_box_2, 0, 2)
        grid.addWidget(self.spin_box_3, 0, 3)

    def get_lower_limit(self):
        """Метод возвращает минимальное значение спин бокса"""
        return self.lower_limit

    def get_top_limit(self):
        """Метод возвращает максимально возможное значение спин бокса"""
        return self.top_limit

    def get_step_limit(self):
        """Метод возвращает максимально возможное значение для шага спин бокса"""
        return self.step_limit

    def set_lower_limit(self, value):
        self.lower_limit = value

    def set_top_limit(self, value):
        self.top_limit = value

    def set_step_limit(self, value):
        self.step_limit = value

    def get_min_value(self):
        """Метод возвращает минимальное значение границы, установленное в спин боксе"""
        return self.spin_box_1.value()

    def get_max_value(self):
        """Метод возвращает максимальное значение, установленное в спин боксе"""
        return self.spin_box_2.value()

    def get_step_value(self):
        """Метод возвращает значение шега, установленное в спин боксе"""
        return self.spin_box_3.value()


def window_choose_params(self, parameters, parent=None):
    def f():
        if parent.window_choose is None:
            self.window_choose = ParamsWindow(parameters, parent=parent)
            self.window_choose.show()

    return f
    # TODO: переделать в pop up


# def add_linear_graph(graph_obj, min_val, max_val, h=1):
#     w = QtWidgets.QWidget()
#     grid = QtWidgets.QGridLayout()
#     btn_delete = QtWidgets.QPushButton()
#     btn_plot = QtWidgets.QPushButton()
#     label = QtWidgets.QLabel()
#     w_range = add_layout_range(graph_obj.get_type(), min_val, max_val, h)
#     grid.addWidget(btn_plot, 0, 0)
#     grid.addWidget(btn_delete, 1, 0)
#     grid.addWidget(label, 0, 1)
#     grid.addWidget(w_range, 1, 1, 1, 3)
#     # grid.addWidget(spin_box_2, 1, 2)
#     # grid.addWidget(spin_box_3, 1, 3)
#     w.setLayout(grid)
#     # self.list_graph.addWidget(w)
#     btn_delete.setText(translate("MainWindow", "Удалить"))
#     btn_plot.setText(translate("MainWindow", "Построить"))
#     label.setText(translate("MainWindow", graph_obj.get_name()))
#
#     btn_delete.clicked.connect(delete_graph(w))
#
#     return w


def add_heat_map():
    w = QtWidgets.QWidget()
    grid = QtWidgets.QGridLayout()
    btn_delete = QtWidgets.QPushButton()
    btn_plot = QtWidgets.QPushButton()
    spin_box_1 = QtWidgets.QSpinBox()
    spin_box_2 = QtWidgets.QSpinBox()
    spin_box_3 = QtWidgets.QSpinBox()
    spin_box_4 = QtWidgets.QSpinBox()
    spin_box_5 = QtWidgets.QSpinBox()
    spin_box_6 = QtWidgets.QSpinBox()
    grid.addWidget(btn_plot, 0, 0)
    grid.addWidget(btn_delete, 1, 0)
    grid.addWidget(spin_box_1, 0, 1)
    grid.addWidget(spin_box_2, 0, 2)
    grid.addWidget(spin_box_3, 0, 3)
    grid.addWidget(spin_box_4, 1, 1)
    grid.addWidget(spin_box_5, 1, 2)
    grid.addWidget(spin_box_6, 1, 3)
    w.setLayout(grid)
    # self.list_graph.addWidget(w)
    btn_delete.setText(translate("MainWindow", "Удалить"))
    btn_plot.setText(translate("MainWindow", "Построить"))

    btn_delete.clicked.connect(delete_graph(w))
    return w


# def get_max_step(self, x1, x2):
#     delta = abs(x2 - x1)
#     return delta

# def get_max_step(sb, w):
#     def f(x1):
#         delta = abs(sb.value() - x1)
#         # print(delta)
#         w.setMaximum(delta)
#         # return abs(x2 - x1)
#
#     return f
