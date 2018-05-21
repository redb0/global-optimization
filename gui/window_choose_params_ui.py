from PyQt5 import QtWidgets, QtCore


class UiParamsWindow:
    """Графический интерфейс окна выбора значений параметра"""
    def __init__(self):
        self.list = None
        self.add_params_to_list_btn = None
        self.reset_btn = None

    def setup_ui(self, window):
        main_layout = QtWidgets.QVBoxLayout()
        self.list = QtWidgets.QListWidget()

        window.setObjectName("ParamsWindow")
        window.resize(325, 300)
        window.setLayout(main_layout)
        h_box = QtWidgets.QHBoxLayout()

        self.add_params_to_list_btn = QtWidgets.QPushButton()
        self.reset_btn = QtWidgets.QPushButton()
        h_box.addWidget(self.add_params_to_list_btn)
        h_box.addWidget(self.reset_btn)

        main_layout.addWidget(self.list)
        main_layout.addLayout(h_box)

        self.retranslate(window)

    def retranslate(self, window):
        window.setWindowTitle(self.translate("ParamsWindow", "Выбор значений параметра"))
        self.add_params_to_list_btn.setText(self.translate("ParamsWindow", "Сохранить выбор"))
        self.reset_btn.setText(self.translate("ParamsWindow", "Сброс"))

    def translate(self, s, s_1: str):
        return QtCore.QCoreApplication.translate(s, s_1)
