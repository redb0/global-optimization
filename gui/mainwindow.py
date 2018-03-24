import copy
from PyQt5.QtWidgets import QMainWindow, QPushButton, QMessageBox, QCheckBox

import AlgorithmParameter
from Settings import Settings
from algorithms.StandardGSA import StandardGSA
from algorithms.StandardSAC import StandardSAC
from graph.PossibleGraph import PossibleGraph

from gui.mainwindow_ui import UiMainWindow


# TODO: сделать чтобы при выборе нескольких алгоритмов выводились общие параметры в комбобоксы \/???
# TODO: сделать видеты для показа возмоных графиков
# TODO: сделать видет для линейного графика, если у показателя диапазон - линейный график, если значения, то точечный
# TODO: сделать классы для потенциальных графиков - линейный, точечный, тепловая карта
# TODO: сделать окно для ввода параметров отдельных алгоритмов
from gui.wdg.LineGraphWidget import LineGraphWidget
from gui.wdg.PointGraphWidget import PointGraphWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = UiMainWindow()

        self.settings = Settings()

        self.active_alg_1 = [StandardGSA(), StandardSAC()]
        self.to_test_list = []

        self.ui.setup_ui(self, self.active_alg_1)

        # self.fill_combobox_2([x.get_full_name() for x in self.active_alg_1], self.ui.combobox_alg)
        self.fill_combobox_2(self.active_alg_1, self.ui.combobox_alg)
        self.ui.add_new_alg_btn.clicked.connect(lambda: self.add_alg())

        self.active_alg = {"StandardGSA": None, "StandardSAC": None}
        self.window_settings_alg = None
        self.window_common_settings = None

        self.window_choose = None
        self.possible_graphics = []

        self.change_status_activity_buttons(self.ui.alg_form, True)

        self.ui.add_linear_graph_btn.clicked.connect(lambda: self.add_linear_graph(self.to_test_list))
        # self.ui.add_heat_map_btn.clicked.connect(self.ui.add_heat_map)

    # def open_settings_alg_window(self):
        # def f():
        #     self.window_choose = ParamsWindow(parameters, parent=parent)
        #     self.window_choose.show()
        # return f
        # pass

    def add_linear_graph(self, alg):  # сюда лучше не передавать алгориты а передавать в функцию на кнопке построить график
        print("--------->", alg)
        # TODO: переименовать переменные, нихрена не понятно
        d = self.get_value_from_combobox(self.ui.param_linear_graph)
        p = AlgorithmParameter.get_parameters(list(d.keys())[0])
        print("Параметр для построения графика: ", list(d.keys())[0])
        if p.allowable_values is not None:
            point_graph = PossibleGraph("POINT_GRAPH", [p], [], alg)
            point_graph_wdg = PointGraphWidget(point_graph)
            self.ui.list_graph.addWidget(point_graph_wdg.get_widget(parent=self))
            # self.ui.list_graph.addStretch(1)
        else:
            line_graph = PossibleGraph("LINE_GRAPH", p, [], [])
            line_graph_wdg = LineGraphWidget(line_graph)
            self.ui.list_graph.addWidget(line_graph_wdg.get_widget(lower_limit=0, top_limit=1000,
                                                                   step_limit=1, get_alg=self.get_active_algorithm,
                                                                   print_error=self.print_error))
            # self.ui.list_graph.addStretch(1)
        # print(self.window_choose)

    def get_value_from_combobox(self, combobox):
        text = combobox.currentText()
        key = combobox.currentData()
        d = {key: text}
        print(d)
        return d

    def check_cb(self):
        """Удалить или переработать"""
        if self.ui.standard_gsa_cb.checkState():
            self.active_alg["StandardGSA"] = StandardGSA()
            # self.ui.standard_gsa_params_btn.setDisabled(False)
        else:
            self.active_alg["StandardGSA"] = None
            # self.ui.standard_gsa_params_btn.setDisabled(True)
        if self.ui.standard_sac_cb.checkState():
            self.active_alg["StandardSAC"] = StandardSAC()
        else:
            self.active_alg["StandardSAC"] = None
        # for i in range(self.ui.alg_form.count()):
        #     item = self.ui.alg_form.itemAt(i).widget()
        #     if type(item) == QCheckBox:
        #         self.ui.alg_form.itemAt(i + 1).widget().setDisabled(not item.checkState())
        data = self.get_params()
        print(data)
        data = self.get_common_params(*data)
        # self.ui.param_linear_graph.clear()
        # self.ui.param_linear_graph.currentText()
        # self.ui.param_linear_graph.currentData()

        self.fill_combobox(data, self.ui.param_linear_graph, self.ui.param_heat_map_1, self.ui.param_heat_map_2)

    def add_parameters_in_combobox(self, get_idx_active_cb):
        def f():
            """
            
            :return: 
            """
            # params = self.get_params(self.to_test_list)
            idx_active_cb = get_idx_active_cb()
            params = self.get_params_on_idx(self.to_test_list, idx_active_cb)
            print(params)
            common_params = self.get_common_params(*params)
            self.fill_combobox(common_params,
                               self.ui.param_linear_graph,
                               self.ui.param_heat_map_1,
                               self.ui.param_heat_map_2)
        return f

    def get_params_on_idx(self, to_test_list, idx_list):
        d = []
        for i in idx_list:
            # alg = self.active_alg.get(i)
            alg = to_test_list[i]
            if alg is not None:
                # abr = alg.get_abbreviation_params()
                p = alg.get_params_dict()
                d.append(p)
        return d

    def get_params(self, to_test_list):
        d = []
        for alg in to_test_list:
            # alg = self.active_alg.get(i)
            if alg is not None:
                # abr = alg.get_abbreviation_params()
                p = alg.get_params_dict()
                d.append(p)
        return d

    def clear_combobox(self, *args):
        for cmb in args:
            cmb.clear()

    def fill_combobox(self, data, *args):
        # TODO: перенести в общие
        for cmb in args:
            cmb.clear()
            for k in data.keys():
                if (k != "EC") and (k != "RN"):
                    cmb.addItem(data.get(k), k)

    def fill_combobox_2(self, data, *args):
        # TODO: перенести в общие
        for cmb in args:
            cmb.clear()
            for k in data:
                cmb.addItem(k.get_full_name(), k)

    def get_common_params(self, *args):
        l = [list(i.keys()) for i in args]
        d = {}
        if not l:
            return d
        common_params_arg = self.get_common_items(*l)
        for x in common_params_arg:
            d.update({x: args[0].get(x)})
        return d

    def get_common_items(self, *args):
        # TODO: перенести в общие
        sets = [set(x) for x in args]
        return list(sets[0].intersection(*sets[1:]))

    def get_active_alg(self):
        # TODO: Добавляются кнопки и чекбосксы для алгоритмов 4
        self.active_alg = []
        if self.ui.standard_gsa_cb.checkState():
            self.active_alg.append("StandardGSA")
        if self.ui.standard_sac_cb.checkState():
            self.active_alg.append("StandardSAC")
        return self.active_alg

    def get_active_algorithm(self):
        return self.to_test_list

    def change_status_activity_buttons(self, layout, flag):
        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if type(item) == QPushButton:
                item.setDisabled(flag)

    def add_alg(self):
        name = self.ui.combobox_alg.currentText()
        alg = self.ui.combobox_alg.currentData()
        a = copy.deepcopy(alg)
        self.to_test_list.append(a)

        cb_handler = self.add_parameters_in_combobox

        # a = copy.deepcopy(alg)
        # a.set_params_value(a.get_parameters(), MI=0)
        # print(a)

        self.ui.add_row_in_form(self.ui.alg_form, a.get_parameters(), name, "Параметризировать", cb_handler, self)

    def print_error(self, text: str) -> None:
        QMessageBox.information(self, 'Внимание!', text,
                                QMessageBox.Cancel, QMessageBox.Cancel)

    # def get_alg(self, list_alg, name):
    #     for a in list_alg:


