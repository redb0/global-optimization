from PyQt5 import QtCore, QtWidgets

# import alg_parameters


class UiAlgorithmSetupWindow:
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
                self.fill_combobox(combobox, s.get_allowable_values())
                self.form.addRow(label, combobox)
            else:
                if s.get_type() == int:
                    spin_box = QtWidgets.QSpinBox()
                    spin_box.setSingleStep(1)
                    # spin_box.setValue(s.get_default_value())
                elif s.get_type() == float:
                    spin_box = QtWidgets.QDoubleSpinBox()
                    spin_box.setSingleStep(0.01)
                spin_box.setMinimum(0)
                spin_box.setMaximum(2000)
                spin_box.setValue(s.get_default_value())
                self.form.addRow(label, spin_box)

        self.apply_btn = QtWidgets.QPushButton()
        self.close_btn = QtWidgets.QPushButton()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.apply_btn)
        h_box.addWidget(self.close_btn)
        main_layout.addLayout(h_box)

        self.retranslate(window)

    # def save_settings(self, settings):
    #
    #     for i in range(self.form.count()):
    #         item = self.form.itemAt(i).widget()
    #         if type(item) == QtWidgets.QSpinBox:
    #             name = self.form.itemAt(i - 1).widget().text()
    #             value = item.value()
    #             s = alg_parameters.get_param_on_name(settings, name)
    #             s.set_selected_values(value)
    #         elif type(item) == QtWidgets.QDoubleSpinBox:
    #             name = self.form.itemAt(i - 1).widget().text()
    #             value = item.value()
    #             s = alg_parameters.get_param_on_name(settings, name)
    #             s.set_selected_values(value)
    #         elif type(item) == QtWidgets.QComboBox:
    #             name = self.form.itemAt(i - 1).widget().text()
    #             value = item.currentText()
    #             s = alg_parameters.get_param_on_name(settings, name)
    #             s.set_selected_values(value)

    def fill_combobox(self, cmb, data):
        cmb.clear()
        for k in data:
            cmb.addItem(str(k))

    def retranslate(self, window):
        window.setWindowTitle(self.translate("SetupAlgWindow", "Параметры алгоритма"))
        self.close_btn.setText(self.translate("SetupAlgWindow", "Закрыть"))
        self.apply_btn.setText(self.translate("SetupAlgWindow", "Применить"))

    def translate(self, s, s_1: str):
        return QtCore.QCoreApplication.translate(s, s_1)
