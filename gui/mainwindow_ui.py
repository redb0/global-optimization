from PyQt5 import QtWidgets, QtCore

from gui.AlgorithmSetupWindow import AlgorithmSetupWindow


class UiMainWindow:
    def __init__(self):
        self.menuFile = None
        self.menuSettings = None
        self.menuHelp = None
        self.statusBar = None

    def setup_ui(self, main_window, alg_list):
        main_window.setObjectName("MainWindow")
        main_window.resize(800, 600)

        central_wdg = QtWidgets.QWidget()
        main_window.setCentralWidget(central_wdg)

        menu_bar = QtWidgets.QMenuBar(main_window)
        menu_bar.setObjectName("menu_bar")

        # Файл
        self.menuFile = QtWidgets.QMenu(menu_bar)
        self.menuFile.setObjectName("menuFile")
        # Настройки
        self.menuSettings = QtWidgets.QMenu(menu_bar)
        self.menuSettings.setObjectName("menuSettings")
        # Помощь
        self.menuHelp = QtWidgets.QMenu(menu_bar)
        self.menuHelp.setObjectName("menuHelp")

        main_window.setMenuBar(menu_bar)

        self.statusBar = QtWidgets.QStatusBar(main_window)
        self.statusBar.setObjectName("statusBar")
        main_window.setStatusBar(self.statusBar)

        self.actionOpenJson = QtWidgets.QAction(main_window)
        self.actionOpenJson.setObjectName("actionOpenJson")

        self.actionOpenDBJson = QtWidgets.QAction(main_window)
        self.actionOpenDBJson.setObjectName("actionOpenDBJson")

        # self.actionSave = QtWidgets.QAction(main_window)
        # self.actionSave.setObjectName("actionSave")

        self.actionQuit = QtWidgets.QAction(main_window)
        self.actionQuit.setObjectName("actionQuit")

        self.actionSettings = QtWidgets.QAction(main_window)
        self.actionSettings.setObjectName("actionSettings")

        self.actionAbout = QtWidgets.QAction(main_window)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelp = QtWidgets.QAction(main_window)
        self.actionHelp.setObjectName("actionHelp")

        self.menuFile.addAction(self.actionOpenJson)
        # self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        menu_bar.addAction(self.menuFile.menuAction())

        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        menu_bar.addAction(self.menuHelp.menuAction())

        self.menuSettings.addAction(self.actionSettings)
        menu_bar.addAction(self.menuSettings.menuAction())

        main_layout = QtWidgets.QHBoxLayout()
        central_wdg.setLayout(main_layout)

        self.alg_layout = QtWidgets.QVBoxLayout()
        self.graph_layout = QtWidgets.QVBoxLayout()
        # self.graph_settings = QtWidgets.QVBoxLayout()
        # self.graph_settings.addStretch(1)
        # self.params_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(self.alg_layout)
        main_layout.addLayout(self.graph_layout)
        # main_layout.addLayout(self.graph_settings)

        # TODO: Добавляются кнопки и чекбосксы для алгоритмов 1
        self.alg_title = QtWidgets.QLabel()
        # self.standard_gsa_cb = QtWidgets.QCheckBox()
        # self.standard_gsa_params_btn = QtWidgets.QPushButton()
        # self.standard_gsa_params_btn.setMaximumWidth(120)
        # self.standard_sac_cb = QtWidgets.QCheckBox()
        # self.standard_sac_params_btn = QtWidgets.QPushButton()
        # self.standard_sac_params_btn.setMaximumWidth(120)
        # self.params_btn = [self.standard_gsa_params_btn, self.standard_sac_params_btn]

        # TODO: Добавляются кнопки и чекбосксы для алгоритмов 2
        self.alg_form = QtWidgets.QFormLayout()
        self.alg_form.addRow(self.alg_title)

        # for alg in alg_list:
        #     TODO: можно вычислять выбранный алгоритм по номеру в массиве будет такой же как в alg_list, переданный сюда
            # cb = QtWidgets.QCheckBox()
            # btn = QtWidgets.QPushButton()
            # btn.setMaximumWidth(120)
            # self.alg_form.addRow(cb, btn)

        # self.alg_form.addRow(self.standard_gsa_cb, self.standard_gsa_params_btn)
        # self.alg_form.addRow(self.standard_sac_cb, self.standard_sac_params_btn)
        self.alg_layout.addLayout(self.alg_form)

        self.add_new_alg_btn = QtWidgets.QPushButton()
        self.combobox_alg = QtWidgets.QComboBox()
        h_box_3 = QtWidgets.QHBoxLayout()
        h_box_3.addWidget(self.combobox_alg)
        h_box_3.addWidget(self.add_new_alg_btn)
        self.alg_layout.addLayout(h_box_3)

        self.add_linear_graph_btn = QtWidgets.QPushButton()
        self.param_linear_graph = QtWidgets.QComboBox()
        h_box_1 = QtWidgets.QHBoxLayout()
        # v_box_1 = QtWidgets.QVBoxLayout()
        h_box_1.addWidget(self.add_linear_graph_btn)
        h_box_1.addWidget(self.param_linear_graph)

        self.add_heat_map_btn = QtWidgets.QPushButton()
        self.param_heat_map_1 = QtWidgets.QComboBox()
        self.param_heat_map_2 = QtWidgets.QComboBox()
        h_box_2 = QtWidgets.QHBoxLayout()
        v_box_2 = QtWidgets.QVBoxLayout()
        h_box_2.addWidget(self.add_heat_map_btn)
        h_box_2.addLayout(v_box_2)
        v_box_2.addWidget(self.param_heat_map_1)
        v_box_2.addWidget(self.param_heat_map_2)

        self.list_graph = QtWidgets.QVBoxLayout()
        # TODO: Сделать чтобы виджеты при добавлении не растягивались
        # self.list_graph.addStretch(1)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        w = QtWidgets.QWidget()
        w.setLayout(self.list_graph)
        scroll.setWidget(w)

        # self.graph_form.addRow()
        self.graph_layout.addLayout(h_box_1)
        self.graph_layout.addLayout(h_box_2)
        self.graph_layout.addWidget(scroll)
        # self.graph_layout.addLayout(self.list_graph)
        # self.graph_layout.addStretch(1)

        self.retranslate(main_window)

    def retranslate(self, main_window):
        main_window.setWindowTitle(self.translate("MainWindow", "Global Optimization"))
        self.menuFile.setTitle(self.translate("MainWindow", "Файл"))
        # TODO: продумать меню

        self.actionOpenJson.setText(self.translate("MainWindow", "Загрузить функцию"))
        self.actionOpenJson.setStatusTip(self.translate("MainWindow", "Импорт параметров тестовой функции из Json"))
        self.actionOpenJson.setShortcut(self.translate("MainWindow", "Ctrl+O"))
        self.actionOpenDBJson.setText(self.translate("MainWindow", "Выбрать функцию"))
        self.actionOpenDBJson.setStatusTip(self.translate("MainWindow", "Выбрать тестовую функцию из базы Json"))

        # self.actionSave.setText(self.translate("MainWindow", "Сохранить параметры"))
        # self.actionSave.setStatusTip(self.translate("MainWindow", "Сохранить парметры тестовой функции в json файле"))
        self.actionQuit.setText(self.translate("MainWindow", "Выход"))
        self.actionQuit.setShortcut(self.translate("MainWindow", "Ctrl+Q"))

        # Справка
        self.menuHelp.setTitle(self.translate("MainWindow", "Справка"))
        self.actionHelp.setText(self.translate("MainWindow", "Справка"))
        self.actionHelp.setShortcut(self.translate("MainWindow", "F1"))
        self.actionAbout.setText(self.translate("MainWindow", "О программе"))

        # Настройки
        self.menuSettings.setTitle(self.translate("MainWindow", "Настройки"))
        self.actionSettings.setText(self.translate("MainWindow", "Настройки"))
        # self.actionOpenDocker.setText(self.translate("MainWindow", "Показать докеры"))

        # TODO: Добавляются кнопки и чекбосксы для алгоритмов 3
        self.alg_title.setText(self.translate("MainWindow", "Алгоритмы"))
        # self.standard_gsa_cb.setText(self.translate("MainWindow", "Гравитационный поиск"))
        # self.standard_sac_cb.setText(self.translate("MainWindow", "Метод селективного усреднения"))

        self.add_linear_graph_btn.setText(self.translate("MainWindow", "Добавить линейный график"))
        self.add_heat_map_btn.setText(self.translate("MainWindow", "Добавить тепловую карту"))

        self.add_new_alg_btn.setText(self.translate("MainWindow", "Добавить алгоритм"))

        # for btn in self.params_btn:
        #     btn.setText(self.translate("MainWindow", "Параметризировать"))

    def translate(self, s, s_1: str):
        return QtCore.QCoreApplication.translate(s, s_1)

    def add_row_in_form(self, form, settings_list, text, text_btn, cb_handler, window):
        """

        :param cb_handler: 
        :param settings_list: 
        :param window: 
        :param form:
        :param text:
        :param text_btn:
        :return:
        """
        cb = QtWidgets.QCheckBox()
        btn = QtWidgets.QPushButton()
        delete_btn = QtWidgets.QPushButton()
        btn.setMaximumWidth(120)
        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(btn)
        h_box.addWidget(delete_btn)
        # idx = form.rowCount()
        form.addRow(cb, h_box)
        cb.setText(self.translate("MainWindow", text))
        btn.setText(self.translate("MainWindow", text_btn))
        delete_btn.setText(self.translate("MainWindow", "Удалить"))
        delete_btn.clicked.connect(self.delete_row(form, cb))
        btn.setDisabled(True)
        btn.clicked.connect(self.open_settings_alg_window(settings_list, text, parent=window))
        cb.stateChanged.connect(btn.setEnabled)
        cb.stateChanged.connect(cb_handler(self.get_index_active_checkbox(form)))
        # delete_btn.setDisabled(True)

    def get_index_active_checkbox(self, form):
        def f():
            idx = []
            for i in range(form.count()):
                item = form.itemAt(i).widget()
                if type(item) == QtWidgets.QCheckBox:
                    if item.checkState():
                        j = int((i - 1) / 2)
                        idx.append(j)
            print(idx)
            return idx
        return f

    def delete_row(self, form, cb):
        """
        Удаление строки в форме.
        
        Возвращает функцию, 
        удаляющую строку в форме, если строка содержит переданный чекбокс.
        :param form: форма из которой необходимо удалить строку, QFormLayout 
        :param cb: чекбокс, строку с которым необходимо удалить, QCheckBox
        :return: функция, которая замыкается на аргументах form и cb и удаляет строку
        """
        def f():
            """
            Функция-замыкание. Удаляет строку из формы.
            :return: None
            """
            idx = form.indexOf(cb)
            idx = (idx - 1) / 2 + 1
            form.removeRow(idx)
        return f

    def open_settings_alg_window(self, settings_list, alg_name, parent=None):
        def f():
            if parent.window_settings_alg is None:
                parent.window_settings_alg = AlgorithmSetupWindow(settings_list, alg_name, parent=parent)
                parent.window_settings_alg.show()
        return f
        pass
