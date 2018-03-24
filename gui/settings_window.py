from PyQt5 import QtCore

from PyQt5.QtWidgets import QWidget

from Settings import Settings, get_attributes
from gui.settings_window_ui import UiSettingsWindow


class SettingsWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent, QtCore.Qt.Window)

        self.ui = UiSettingsWindow()

        self.settings_list = list(get_attributes(Settings).values())

        self.ui.setup_ui(self, self.settings_list)

        # self.ui.close_btn.clicked.connect(self.closeEvent)  # переопределение встроенного обработчика
        self.ui.save_btn.clicked.connect(self.save_settings)
        self.ui.reset_btn.clicked.connect(self.reset)

    def save_settings(self):
        Settings.min_flag = self.ui.min_flag.value()
        Settings.number_of_runs = self.ui.number_runs.value()
        Settings.epsilon = float(self.ui.epsilon.text())  # epsilon пока поддерживать только одинарные значения. без списков
        Settings.abs_path_test_func = self.ui.abs_path_test_func_te.text()
        Settings.legend_position = self.ui.legend_position_te.text()

    def reset(self):
        for s in self.settings_list:
            s.set_default_value()

    def closeEvent(self, e):
        self.parent().window_common_settings = None
        self.close()
