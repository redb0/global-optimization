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

        self.spin_box_1 = None
        self.spin_box_2 = None
        self.spin_box_3 = None

        self.setup_ui()

    def setup_ui(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        if self.type_p == int:
            self.spin_box_1 = QtWidgets.QSpinBox()
            self.spin_box_2 = QtWidgets.QSpinBox()
            self.spin_box_3 = QtWidgets.QSpinBox()
            self.spin_box_3.setSingleStep(self.step_limit)
        elif self.type_p == float:
            self.spin_box_1 = QtWidgets.QDoubleSpinBox()
            self.spin_box_2 = QtWidgets.QDoubleSpinBox()
            self.spin_box_3 = QtWidgets.QDoubleSpinBox()
            self.spin_box_3.setSingleStep(0.1)

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
