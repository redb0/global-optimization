import json

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QMessageBox, QCheckBox

from Settings import Settings, get_attributes, set_all_default_values
from gui.settings_window_ui import UiSettingsWindow

import support_func


class SettingsWindow(QWidget):
    """Окно общих настроек. Вызывается по нажатию на кнопку "Настройки" в меню приложения."""
    def __init__(self, parent):
        super().__init__(parent, QtCore.Qt.Window)

        self.ui = UiSettingsWindow()

        self.settings = Settings()

        self.settings_list = list(get_attributes(Settings).values())

        self.ui.setup_ui(self, self.settings_list)

        for g in self.settings.additional_graphics:
            cb = QCheckBox(g['name'])
            cb.setChecked(g['draw'])
            self.ui.box_layout.addWidget(cb)
        self.ui.box_layout.addStretch(1)

        # self.ui.close_btn.clicked.connect(self.closeEvent)  # переопределение встроенного обработчика
        self.ui.save_btn.clicked.connect(self.save_settings)
        self.ui.reset_btn.clicked.connect(self.reset)
        self.ui.open_file_btn.clicked.connect(self.open_file_dialog)

        self.setup_settings()

    def setup_settings(self):
        self.ui.abs_path_test_func_te.setText(self.settings.abs_path_test_func)
        self.ui.min_flag.setValue(self.settings.min_flag)
        self.ui.number_runs.setValue(self.settings.number_of_runs)
        self.ui.epsilon.setText(str(self.settings.epsilon))
        self.ui.legend_position_top.setChecked(self.settings.legend_position == "top")
        self.ui.legend_position_right.setChecked(self.settings.legend_position == "right")
        self.ui.global_min.setText(str(self.settings.global_min))
        self.ui.global_max.setText(str(self.settings.global_max))
        self.ui.dimension.setText(str(self.settings.dimension))
        self.ui.report_cb.setChecked(self.settings.report)
        for i in range(self.ui.box_layout.count()):
            wdg = self.ui.box_layout.itemAt(i).widget()
            if type(wdg) == QCheckBox:
                wdg.setChecked(self.settings.additional_graphics[i]['draw'])

    def save_settings(self):
        """Сохранение общих настроек. Действие по клику на кнопку "Сохранить"."""
        # TODO: возможно стоит перенести вывод ошибок прямо в Settings и отказаться от property
        if self.ui.abs_path_test_func_te.text() != "":
            self.settings.abs_path_test_func = self.ui.abs_path_test_func_te.text()
        else:
            self.print_error("Не указано расположение файла тестовой функции.")
            return
        if self.ui.min_flag.value() in [0, 1]:
            self.settings.min_flag = self.ui.min_flag.value()
        else:
            self.print_error("Недопустимое значения флага минимизации. Установлено значение по умолчанию (1)")
            return
        if self.ui.number_runs.value() > 0:
            self.settings.number_of_runs = self.ui.number_runs.value()
        else:
            self.print_error("Количество прогонов должно быть больше 0. Установлено значение по умолчанию (100).")
            return
        if float(self.ui.epsilon.text()) > 0:
            self.settings.epsilon = float(self.ui.epsilon.text())  # epsilon пока поддерживать только одинарные значения. без списков
        else:
            self.print_error("Epsilon должно быть больше 0. Установлено значение по умолчанию (0.5).")
            return
        if self.ui.legend_position_top.isChecked():  # "left", "bottom"
            self.settings.legend_position = "top"
        elif self.ui.legend_position_right.isChecked():
            self.settings.legend_position = "right"
        else:
            self.print_error("Некорректное расположение легенды. Установлено значение по умолчанию (top)")
            return
        if self.ui.global_min.text() != str(None):
            self.settings.global_min = json.loads(self.ui.global_min.text())
        if self.ui.global_max.text() != str(None):
            self.settings.global_max = json.loads(self.ui.global_max.text())
        if self.ui.dimension.text() != "0":
            self.settings.dimension = int(self.ui.dimension.text())
        self.settings.report = self.ui.report_cb.isChecked()

        for i in range(self.ui.box_layout.count()):
            wdg = self.ui.box_layout.itemAt(i).widget()
            if type(wdg) == QCheckBox:
                self.settings.additional_graphics[i]['draw'] = wdg.isChecked()
        # print(self.settings.additional_graphics)

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
        # self.ui.legend_position_te.setText(self.settings.legend_position)
        self.ui.legend_position_top.setChecked(True)
        self.ui.dimension.setText(str(self.settings.dimension))
        self.ui.global_min.setText(str(self.settings.global_min))
        self.ui.global_max.setText(str(self.settings.global_max))

        self.ui.report_cb.setChecked(True)

    def closeEvent(self, e):
        self.parent().window_common_settings = None
        self.close()

    def open_file_dialog(self) -> None:
        """
        Метод открытия окна для выбора json-файла с информацией о тестовой функции.
        :return: 
        """
        file_name = support_func.open_file_dialog("Открыть файл тестовой функции",
                                                  "All Files (*);;JSON Files (*.json)", self)
        if file_name:
            self.ui.abs_path_test_func_te.setText(file_name)
            data = support_func.read_json(file_name)
            self.ui.dimension.setText(str(data["dimension"]))
            self.ui.global_min.setText(str(data["global_min"]))
            self.ui.global_max.setText(str(data["global_max"]))

    def print_error(self, text: str) -> None:
        QMessageBox.information(self, 'Внимание!', text,
                                QMessageBox.Cancel, QMessageBox.Cancel)

