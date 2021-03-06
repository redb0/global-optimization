from PyQt5 import QtCore, QtWidgets


class UiSettingsWindow:
    """Класс графического интерфейса окна общих настроек."""
    def __init__(self):
        self.save_btn = None
        self.reset_btn = None

        self.form = None

    def setup_ui(self, window, settings):
        main_layout = QtWidgets.QVBoxLayout()

        window.setObjectName("SettingsWindow")
        window.resize(325, 300)
        window.setLayout(main_layout)

        h_box = QtWidgets.QHBoxLayout()
        self.form = QtWidgets.QFormLayout()

        # TODO: вставить значеняия по умолчанию
        self.min_flag_label = QtWidgets.QLabel()
        self.min_flag = QtWidgets.QSpinBox()
        self.min_flag.setMinimum(0)
        self.min_flag.setMaximum(1)
        self.min_flag.setValue(1)

        self.number_runs_label = QtWidgets.QLabel()
        self.number_runs = QtWidgets.QSpinBox()
        self.number_runs.setMinimum(0)
        self.number_runs.setMaximum(5000)
        self.number_runs.setValue(100)

        self.epsilon_label = QtWidgets.QLabel()
        self.epsilon = QtWidgets.QLineEdit()
        self.epsilon.setText("0.5")

        self.abs_path_test_func_label = QtWidgets.QLabel()
        self.abs_path_test_func_te = QtWidgets.QLineEdit()
        self.abs_path_test_func_te.setReadOnly(True)
        self.open_file_btn = QtWidgets.QPushButton()
        wgt = QtWidgets.QWidget()
        h_box_1 = QtWidgets.QHBoxLayout()
        h_box_1.addWidget(self.abs_path_test_func_te)
        h_box_1.addWidget(self.open_file_btn)
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.abs_path_test_func_label)
        v_box.addLayout(h_box_1)
        wgt.setLayout(v_box)

        self.legend_position_label = QtWidgets.QLabel()
        self.legend_position_top = QtWidgets.QRadioButton()
        self.legend_position_top.setChecked(True)
        self.legend_position_right = QtWidgets.QRadioButton()
        h_box_2 = QtWidgets.QHBoxLayout()
        h_box_2.addWidget(self.legend_position_top)
        h_box_2.addWidget(self.legend_position_right)
        v_box.addWidget(self.legend_position_label)
        v_box.addLayout(h_box_2)
        v_box.addStretch(1)

        self.global_min_label = QtWidgets.QLabel()
        self.global_min = QtWidgets.QLineEdit()
        self.global_max_label = QtWidgets.QLabel()
        self.global_max = QtWidgets.QLineEdit()
        self.dimension_label = QtWidgets.QLabel()
        self.dimension = QtWidgets.QLabel()
        self.report_cb = QtWidgets.QCheckBox()
        self.report_cb.setChecked(True)

        self.form.addRow(self.dimension_label, self.dimension)
        self.form.addRow(self.global_min_label, self.global_min)
        self.form.addRow(self.global_max_label, self.global_max)
        self.form.addRow(self.min_flag_label, self.min_flag)
        self.form.addRow(self.number_runs_label, self.number_runs)
        self.form.addRow(self.epsilon_label, self.epsilon)

        self.save_btn = QtWidgets.QPushButton()
        self.reset_btn = QtWidgets.QPushButton()
        h_box.addWidget(self.save_btn)
        h_box.addWidget(self.reset_btn)

        main_layout.addWidget(wgt)
        main_layout.addLayout(self.form)

        self.groupBox_0 = QtWidgets.QGroupBox()
        v_box_1 = QtWidgets.QVBoxLayout()
        v_box_1.addWidget(self.report_cb)
        v_box_1.addStretch(1)
        self.groupBox_0.setLayout(v_box_1)
        main_layout.addWidget(self.groupBox_0)

        self.groupBox = QtWidgets.QGroupBox()
        self.box_layout = QtWidgets.QVBoxLayout()
        self.groupBox.setLayout(self.box_layout)
        main_layout.addWidget(self.groupBox)
        main_layout.addStretch(1)
        main_layout.addLayout(h_box)

        self.retranslate(window)

    def retranslate(self, window):
        window.setWindowTitle(self.translate("SettingsWindow", "Общие настройки"))
        self.min_flag_label.setText(self.translate("SettingsWindow", "Тип задачи"))
        self.number_runs_label.setText(self.translate("SettingsWindow", "Количество пусков алгоритма"))
        self.epsilon_label.setText(self.translate("SettingsWindow", "Размер epsilon-окрестности"))
        self.abs_path_test_func_label.setText(self.translate("SettingsWindow", "Тестовая функция"))
        self.legend_position_label.setText(self.translate("SettingsWindow", "Положение легенда на графике"))
        self.legend_position_top.setText(self.translate("SettingsWindow", "Сверху"))
        self.legend_position_right.setText(self.translate("SettingsWindow", "Справа"))

        self.global_min_label.setText(self.translate("SettingsWindow", "Координаты глобального минимума"))
        self.global_max_label.setText(self.translate("SettingsWindow", "Координаты глобального максимума"))

        self.dimension_label.setText(self.translate("SettingsWindow", "Размерность задачи"))
        self.dimension.setText(self.translate("SettingsWindow", "0"))
        self.global_min.setText(self.translate("SettingsWindow", "None"))
        self.global_max.setText(self.translate("SettingsWindow", "None"))

        self.groupBox.setTitle(self.translate("SettingsWindow", "Дополнительные графики"))
        self.groupBox_0.setTitle(self.translate("SettingsWindow", "Json-отчет"))

        self.report_cb.setText(self.translate("SettingsWindow", "Время выполнения и количество итераций"))

        self.save_btn.setText(self.translate("SettingsWindow", "Сохранить"))
        self.reset_btn.setText(self.translate("SettingsWindow", "Сбросить"))
        self.open_file_btn.setText(self.translate("SettingsWindow", "Открыть"))

    def translate(self, text, text1: str):
        return QtCore.QCoreApplication.translate(text, text1)
