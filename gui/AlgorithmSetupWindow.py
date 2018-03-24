from PyQt5 import QtWidgets, QtCore

import AlgorithmParameter
from gui.AlgorithmSetupWindow_ui import UiAlgorithmSetupWindow
from support_func import deprecated


class AlgorithmSetupWindow(QtWidgets.QWidget):
    def __init__(self, settings_list, alg_name, parent=None):
        # TODO: сделать чтобы при повторном открытии окна параметры оставались такие как установлены ранее
        super().__init__(parent, QtCore.Qt.Window)

        self.ui = UiAlgorithmSetupWindow()
        self.ui.setup_ui(self, settings_list, alg_name)

        # self.parent = parent

        # self.ui.close_btn.clicked.connect(self.changeEvent)  # удалить строку
        # некорректно работает закрытие на крестик, если переопределить closeEvent, то так тоже будет работать
        # self.ui.close_btn.clicked.connect(lambda: self.close_window())
        self.ui.close_btn.clicked.connect(self.closeEvent)  # переопределение встроенного обработчика
        self.ui.apply_btn.clicked.connect(self.save_settings(settings_list))

    def save_settings(self, settings):
        def f():
            for i in range(self.ui.form.count()):
                item = self.ui.form.itemAt(i).widget()
                if type(item) == QtWidgets.QSpinBox:
                    name = self.ui.form.itemAt(i - 1).widget().text()
                    value = item.value()
                    s = AlgorithmParameter.get_param_on_name(settings, name)
                    s.set_selected_values(value)
                    # print(s.get_selected_values())
                elif type(item) == QtWidgets.QDoubleSpinBox:
                    name = self.ui.form.itemAt(i - 1).widget().text()
                    value = round(item.value(), 2)
                    s = AlgorithmParameter.get_param_on_name(settings, name)
                    s.set_selected_values(value)
                    # print(s.get_selected_values())
                elif type(item) == QtWidgets.QComboBox:
                    name = self.ui.form.itemAt(i - 1).widget().text()
                    value = item.currentText()
                    s = AlgorithmParameter.get_param_on_name(settings, name)
                    s.set_selected_values(value)
                    # print(s.get_selected_values())
            for p in self.parent().to_test_list[0].get_parameters():
                print(p.get_selected_values())
            # settings.clear()
            # settings.append(self.parent().to_test_list[0].get_parameters())
            # print(self.parent().to_test_list[0].get_parameters())
        return f

    @deprecated(message="Вызывает некорректное закрытие по крестику. После чего не открываются окна.")
    def close_window(self):
        self.parent().window_settings_alg = None
        self.close()

    def closeEvent(self, event):
        self.parent().window_settings_alg = None
        self.close()

        # if event:
        #     event.accept()
        # else:
        #     self.close()



