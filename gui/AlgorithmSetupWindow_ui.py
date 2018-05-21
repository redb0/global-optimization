from PyQt5 import QtCore, QtWidgets

from support_func import fill_combobox_list


class UiAlgorithmSetupWindow:
    """Графический интерфейс окна настроек алгоритма"""
    def __init__(self):
        self.title_label = None
        self.form = None
        self.apply_btn = None
        self.close_btn = None

    def setup_ui(self, window, settings, name_alg):
        window.setObjectName("SetupAlgWindow")
        window.resize(325, 300)
        main_layout = QtWidgets.QVBoxLayout()
        window.setLayout(main_layout)

        self.title_label = QtWidgets.QLabel()
        self.title_label.setText(self.translate("SetupAlgWindow", "Введите настройки алгоритма " + name_alg))
        main_layout.addWidget(self.title_label)

        self.form = QtWidgets.QFormLayout()
        main_layout.addLayout(self.form)

        for s in settings:
            label = QtWidgets.QLabel()
            label.setText(self.translate("SetupAlgWindow", s.get_name()))

            if (s.get_allowable_values() is not None) or (s.get_type() == bool):
                combobox = QtWidgets.QComboBox()
                fill_combobox_list(combobox, s.get_allowable_values())
                self.form.addRow(label, combobox)
                index = combobox.findText(str(s.get_selected_values()))
                if index != -1:
                    combobox.setCurrentIndex(index)
            else:
                if s.get_type() == int:
                    spin_box = QtWidgets.QSpinBox()
                    spin_box.setSingleStep(1)
                elif s.get_type() == float:
                    spin_box = QtWidgets.QDoubleSpinBox()
                    spin_box.setSingleStep(0.01)
                spin_box.setMinimum(0)
                spin_box.setMaximum(2000)
                spin_box.setValue(s.get_selected_values())
                self.form.addRow(label, spin_box)

        self.apply_btn = QtWidgets.QPushButton()
        self.close_btn = QtWidgets.QPushButton()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.apply_btn)
        h_box.addWidget(self.close_btn)
        main_layout.addLayout(h_box)

        self.retranslate(window)

    def retranslate(self, window):
        window.setWindowTitle(self.translate("SetupAlgWindow", "Параметры алгоритма"))
        self.close_btn.setText(self.translate("SetupAlgWindow", "Закрыть"))
        self.apply_btn.setText(self.translate("SetupAlgWindow", "Применить"))

    def translate(self, s, s_1: str):
        return QtCore.QCoreApplication.translate(s, s_1)
