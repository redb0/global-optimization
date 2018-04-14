from PyQt5 import QtCore

from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox

from Settings import Settings, get_attributes, set_all_default_values
from gui.settings_window_ui import UiSettingsWindow


class SettingsWindow(QWidget):
    """Окно общих настроек. Вызывается по нажатию на кнопку "Настройки" в меню приложения."""
    def __init__(self, parent):
        super().__init__(parent, QtCore.Qt.Window)

        self.ui = UiSettingsWindow()

        self.settings = Settings()

        self.settings_list = list(get_attributes(Settings).values())

        self.ui.setup_ui(self, self.settings_list)

        # self.ui.close_btn.clicked.connect(self.closeEvent)  # переопределение встроенного обработчика
        self.ui.save_btn.clicked.connect(self.save_settings)
        self.ui.reset_btn.clicked.connect(self.reset)
        self.ui.open_file_btn.clicked.connect(self.open_file_dialog)

    def save_settings(self):
        """Сохранение общих настроек. Действие по клику на кнопку "Сохранить"."""
        # TODO: возможно стоит перенести вывод ошибок прямо в Settings и отказаться от property
        if self.ui.min_flag.value() in [0, 1]:
            self.settings.min_flag = self.ui.min_flag.value()
        else:
            self.print_error("Недопустимое значения флага минимизации. Установлено значение по умолчанию (1)")
        if self.ui.number_runs.value() > 0:
            self.settings.number_of_runs = self.ui.number_runs.value()
        else:
            self.print_error("Количество прогонов должно быть больше 0. Установлено значение по умолчанию (100).")
        if float(self.ui.epsilon.text()) > 0:
            self.settings.epsilon = float(self.ui.epsilon.text())  # epsilon пока поддерживать только одинарные значения. без списков
        else:
            self.print_error("Epsilon должно быть больше 0. Установлено значение по умолчанию (0.5).")
        if self.ui.abs_path_test_func_te.text() != "":
            self.settings.abs_path_test_func = self.ui.abs_path_test_func_te.text()
        else:
            self.print_error("Не указано расположение файла тестовой функции.")
        if self.ui.legend_position_te.text() in ["top", "left", "bottom", "right"]:
            self.settings.legend_position = self.ui.legend_position_te.text()
        else:
            self.print_error("Некорректное расположение легенды. Установлено значение по умолчанию (top)")

    def reset(self) -> None:
        """
        Сброс всех настроек до значения по умолчанию.
        :return: 
        """
        set_all_default_values(Settings)
        self.ui.min_flag.setValue(self.settings.min_flag)
        self.ui.number_runs.setValue(self.settings.number_of_runs)
        self.ui.epsilon.setText(str(self.settings.epsilon))  # epsilon пока поддерживать только одинарные значения. без списков
        self.ui.abs_path_test_func_te.setText(self.settings.abs_path_test_func)
        self.ui.legend_position_te.setText(self.settings.legend_position)

    def closeEvent(self, e):
        self.parent().window_common_settings = None
        self.close()

    def open_file_dialog(self) -> None:
        """
        Метод открытия окна для выбора json-файла с информацией о тестовой функции.
        :return: 
        """
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "All Files (*);;JSON Files (*.json)", options=options)
        if file_name:
            self.ui.abs_path_test_func_te.setText(file_name)

    def print_error(self, text: str) -> None:
        QMessageBox.information(self, 'Внимание!', text,
                                QMessageBox.Cancel, QMessageBox.Cancel)

