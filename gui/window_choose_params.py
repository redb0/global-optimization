from PyQt5 import QtWidgets, QtCore

from gui.window_choose_params_ui import UiParamsWindow


class ParamsWindow(QtWidgets.QWidget):
    # TODO: возможно заменить на pop up
    def __init__(self, parameter, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.ui = UiParamsWindow()
        self.ui.setup_ui(self)

        self.ar = []
        self.p = parameter

        # parent.choose_params = []

        self.fill_list_widget(self.ui.list, self.p.get_allowable_values())

        self.ui.add_params_to_list_btn.clicked.connect(self.add_to_list(self.ui.list, self.p.get_allowable_values()))
        self.ui.reset_btn.clicked.connect(self.reset_widget(self.ui.list))

    def fill_list_widget(self, widget, parameters):
        # TODO: добавить переменную название значения, для вывода "Функция 1" ... или недобавлять
        for p in parameters:
            item = QtWidgets.QListWidgetItem(str(p))
            # could be Qt.Unchecked; setting it makes the check appear
            item.setCheckState(QtCore.Qt.Unchecked)
            widget.addItem(item)

    def add_to_list(self, widget, p):  # widget
        # if item.checkState():
        #     self.ar.append(item.text())
        #     print(self.ar)
        def f():
            values = []
            for i in range(widget.count()):
                if widget.item(i).checkState():
                    values.append(p[i])
                    # print(i)
            # print(self.ar)
            self.p.set_selected_values(values)
            # self.parent().window_choose = self.ar
            print(self.p.get_selected_values())
        return f

    def reset_widget(self, widget):
        # return lambda : widget.item(i).setCheckState(QtCore.Qt.Unchecked) for i in range(widget.count())
        def f():
            for i in range(widget.count()):
                widget.item(i).setCheckState(QtCore.Qt.Unchecked)
        return f
