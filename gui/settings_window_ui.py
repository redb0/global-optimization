from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout, QLabel, QSpinBox, QLineEdit, QWidget


class UiSettingsWindow:
    """Класс графического интерфейса окна общих настроек."""
    def __init__(self):
        self.save_btn = None
        self.reset_btn = None

        self.form = None

    def setup_ui(self, window, settings):
        main_layout = QVBoxLayout()

        window.setObjectName("SettingsWindow")
        window.resize(325, 300)
        window.setLayout(main_layout)

        h_box = QHBoxLayout()
        self.form = QFormLayout()

        # TODO: вставить значеняия по умолчанию
        self.min_flag_label = QLabel()
        self.min_flag = QSpinBox()
        self.min_flag.setMinimum(0)
        self.min_flag.setMaximum(1)
        self.min_flag.setValue(1)

        self.number_runs_label = QLabel()
        self.number_runs = QSpinBox()
        self.number_runs.setMinimum(0)
        self.number_runs.setMaximum(5000)
        self.number_runs.setValue(100)

        self.epsilon_label = QLabel()
        self.epsilon = QLineEdit()
        self.epsilon.setText("0.5")

        self.abs_path_test_func_label = QLabel()
        self.abs_path_test_func_te = QLineEdit()
        self.abs_path_test_func_te.setReadOnly(True)
        self.open_file_btn = QPushButton()
        wgt = QWidget()
        h_box_1 = QHBoxLayout()
        h_box_1.addWidget(self.abs_path_test_func_te)
        h_box_1.addWidget(self.open_file_btn)
        wgt.setLayout(h_box_1)

        self.legend_position_label = QLabel()
        # TODO: сделать радиокнопку с двумя флагами: сверху и справа
        self.legend_position_te = QLineEdit()

        self.form.addRow(self.min_flag_label, self.min_flag)
        self.form.addRow(self.number_runs_label, self.number_runs)
        self.form.addRow(self.epsilon_label, self.epsilon)
        self.form.addRow("", self.abs_path_test_func_label)
        self.form.addRow("", wgt)
        self.form.addRow(self.legend_position_label, self.legend_position_te)

        self.save_btn = QPushButton()
        self.reset_btn = QPushButton()
        h_box.addWidget(self.save_btn)
        h_box.addWidget(self.reset_btn)

        main_layout.addLayout(self.form)
        main_layout.addLayout(h_box)

        self.retranslate(window)

    def retranslate(self, window):
        window.setWindowTitle(self.translate("SettingsWindow", "Общие настройки"))
        self.min_flag_label.setText(self.translate("SettingsWindow", "Тип задачи"))
        self.number_runs_label.setText(self.translate("SettingsWindow", "Количество пусков алгоритма"))
        self.epsilon_label.setText(self.translate("SettingsWindow", "Размер epsilon-окрестности"))
        self.abs_path_test_func_label.setText(self.translate("SettingsWindow", "Тестовая функция"))
        self.legend_position_label.setText(self.translate("SettingsWindow", "Положение легенда на графике"))
        self.legend_position_te.setText(self.translate("SettingsWindow", "top"))

        self.save_btn.setText(self.translate("SettingsWindow", "Сохранить"))
        self.reset_btn.setText(self.translate("SettingsWindow", "Сбросить"))
        self.open_file_btn.setText(self.translate("SettingsWindow", "Открыть"))

    def translate(self, text, text1: str):
        return QtCore.QCoreApplication.translate(text, text1)
