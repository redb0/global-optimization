from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout, QLabel, QSpinBox, QLineEdit, QWidget, \
    QRadioButton, QCheckBox, QGroupBox


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
        v_box = QVBoxLayout()
        v_box.addWidget(self.abs_path_test_func_label)
        v_box.addLayout(h_box_1)
        # v_box.addStretch(1)
        wgt.setLayout(v_box)

        self.legend_position_label = QLabel()
        # self.legend_position_te = QLineEdit()
        self.legend_position_top = QRadioButton()
        self.legend_position_top.setChecked(True)
        self.legend_position_right = QRadioButton()
        h_box_2 = QHBoxLayout()
        h_box_2.addWidget(self.legend_position_top)
        h_box_2.addWidget(self.legend_position_right)
        # legend = QVBoxLayout()
        v_box.addWidget(self.legend_position_label)
        v_box.addLayout(h_box_2)
        v_box.addStretch(1)

        self.global_min_label = QLabel()
        self.global_min = QLineEdit()
        self.global_max_label = QLabel()
        self.global_max = QLineEdit()
        self.dimension_label = QLabel()
        self.dimension = QLabel()

        # self.report_label = QLabel()
        # self.convergence_func_value_label = QLabel()
        # self.convergence_coordinates = QLabel()
        # self.dispersion_graph_label = QLabel()
        # self.graph_number_iteration_label = QLabel()
        # self.graph_best_point_motion_label = QLabel()

        self.report_cb = QCheckBox()
        self.report_cb.setChecked(True)

        # self.convergence_coordinates_cb = QCheckBox()
        # self.convergence_coordinates_cb.setChecked(True)
        # self.convergence_func_value_cb = QCheckBox()
        # self.convergence_func_value_cb.setChecked(True)
        # self.dispersion_graph_cb = QCheckBox()
        # self.dispersion_graph_cb.setChecked(True)
        # self.graph_best_point_motion_cb = QCheckBox()
        # self.graph_best_point_motion_cb.setChecked(True)

        self.form.addRow(self.dimension_label, self.dimension)
        self.form.addRow(self.global_min_label, self.global_min)
        self.form.addRow(self.global_max_label, self.global_max)
        self.form.addRow(self.min_flag_label, self.min_flag)
        self.form.addRow(self.number_runs_label, self.number_runs)
        self.form.addRow(self.epsilon_label, self.epsilon)
        # self.form.addRow(self.legend_position_label, self.legend_position_te)

        self.save_btn = QPushButton()
        self.reset_btn = QPushButton()
        h_box.addWidget(self.save_btn)
        h_box.addWidget(self.reset_btn)

        main_layout.addWidget(wgt)
        main_layout.addLayout(self.form)
        # main_layout.addWidget(self.report_cb)

        self.groupBox_0 = QGroupBox()
        v_box_1 = QVBoxLayout()
        v_box_1.addWidget(self.report_cb)
        v_box_1.addStretch(1)
        self.groupBox_0.setLayout(v_box_1)
        main_layout.addWidget(self.groupBox_0)

        self.groupBox = QGroupBox()
        self.box_layout = QVBoxLayout()
        self.groupBox.setLayout(self.box_layout)
        main_layout.addWidget(self.groupBox)

        # main_layout.addWidget(self.convergence_func_value_cb)
        # main_layout.addWidget(self.convergence_coordinates_cb)
        # main_layout.addWidget(self.graph_best_point_motion_cb)
        # main_layout.addWidget(self.dispersion_graph_cb)
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
        # self.legend_position_te.setText(self.translate("SettingsWindow", "top"))
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
        # self.convergence_coordinates_cb.setText(self.translate("SettingsWindow", "График сходимости по координатам"))
        # self.convergence_func_value_cb.setText(self.translate("SettingsWindow", "График сходимости по значениям функции"))
        # self.dispersion_graph_cb.setText(self.translate("SettingsWindow", "График дисперсии"))
        # self.graph_best_point_motion_cb.setText(self.translate("SettingsWindow", "График движения лучшей точки"))

        self.save_btn.setText(self.translate("SettingsWindow", "Сохранить"))
        self.reset_btn.setText(self.translate("SettingsWindow", "Сбросить"))
        self.open_file_btn.setText(self.translate("SettingsWindow", "Открыть"))

    def translate(self, text, text1: str):
        return QtCore.QCoreApplication.translate(text, text1)
