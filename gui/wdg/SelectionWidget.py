from PyQt5 import QtWidgets, QtCore

from gui.window_choose_params import ParamsWindow


class SelectionWidget(QtWidgets.QWidget):
    """Виджет для вызова окна выбора значений"""
    def __init__(self, param, parent=None):
        """
        :param param  : параметр значения которого нужно выбрать
        :param parent : родительский объект
        """
        super().__init__()
        self.param = param
        self.parent = parent

        self.setup_ui()

    def setup_ui(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        label = QtWidgets.QLabel()
        self.btn_choose = QtWidgets.QPushButton()

        grid.addWidget(label, 1, 0)
        grid.addWidget(self.btn_choose, 2, 0)

        label.setText(self.translate("MainWindow", self.param.get_name()))
        self.btn_choose.setText(self.translate("MainWindow", "Выбрать значения"))

        self.btn_choose.clicked.connect(self.window_choose_params(self.param, parent=self.parent))

    def translate(self, s, s_1: str):
        return QtCore.QCoreApplication.translate(s, s_1)

    def window_choose_params(self, parameters, parent=None):
        # TODO: переделать в pop up
        def f():
            if parent.active_window is None:
                self.window_choose = ParamsWindow(parameters, parent=parent)
                self.window_choose.show()
        return f
