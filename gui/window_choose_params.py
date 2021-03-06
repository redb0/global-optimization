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

        self.fill_list_widget(self.ui.list, self.p.get_allowable_values())

        self.ui.add_params_to_list_btn.clicked.connect(self.add_to_list(self.ui.list, self.p.get_allowable_values()))
        self.ui.reset_btn.clicked.connect(self.reset_widget(self.ui.list))

    def fill_list_widget(self, widget, parameters):
        for p in parameters:
            item = QtWidgets.QListWidgetItem(str(p))
            # could be Qt.Unchecked; setting it makes the check appear
            item.setCheckState(QtCore.Qt.Unchecked)
            widget.addItem(item)

    def add_to_list(self, widget, p):
        def f():
            self.parent().selected_value.clear()
            values = []
            for i in range(widget.count()):
                if widget.item(i).checkState():
                    values.append(p[i])
            self.parent().selected_value.append(values)
        return f

    def reset_widget(self, widget):
        def f():
            for i in range(widget.count()):
                widget.item(i).setCheckState(QtCore.Qt.Unchecked)
            self.parent().selected_value.clear()
        return f
