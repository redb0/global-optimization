import copy
import os
import operator

from PyQt5.QtCore import Q_FLAGS
from PyQt5.QtWidgets import QMainWindow, QPushButton, QMessageBox
import numpy as np

import AlgorithmParameter
from Settings import Settings
from algorithms.NoiseResistanceGSA import NoiseResistanceGSA
from algorithms.StandardGSA import StandardGSA
from algorithms.StandardSAC import StandardSAC
from algorithms.SACacsa import AcsaSAC
from graph.LineGraph import motion_point_graph, graph_convergence_coord, line_graph
from graph.PossibleGraph import PossibleGraph
from gui.about_dialog import AboutDialog

from gui.mainwindow_ui import UiMainWindow

from gui.wdg.HeatMapWidget import HeatMapWidget
from gui.wdg.LineGraphWidget import LineGraphWidget
from gui.wdg.PointGraphWidget import PointGraphWidget

from support_func import fill_combobox_list_alg, open_file_dialog, read_json
from test_func import get_test_func


class MainWindow(QMainWindow):
    """Главное окно программы"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = UiMainWindow()

        self.settings = Settings()

        self.active_alg_1 = [StandardGSA(), StandardSAC(), NoiseResistanceGSA(), AcsaSAC()]
        self.to_test_list = []

        self.ui.setup_ui(self, self.active_alg_1)

        fill_combobox_list_alg(self.active_alg_1, self.ui.combobox_alg)
        self.ui.add_new_alg_btn.clicked.connect(lambda: self.add_alg())

        self.window_settings_alg = None
        self.window_common_settings = None

        self.window_choose = None
        self.possible_graphics = []

        self.change_status_activity_buttons(self.ui.alg_form, True)

        self.get_selected_algorithms = self.ui.get_index_active_checkbox(self.ui.alg_form)

        self.ui.actionAbout.triggered.connect(self.open_about_dialog)

        self.ui.add_linear_graph_btn.clicked.connect(self.add_linear_graph)
        self.ui.add_heat_map_btn.clicked.connect(self.add_heat_map)

        self.param_in_combobox_for_heat_map = {}
        self.ui.param_heat_map_1.activated.connect(
            lambda: self.prohibit_duplicate_selection(self.ui.param_heat_map_1, self.ui.param_heat_map_2))
        self.ui.param_heat_map_2.activated.connect(
            lambda: self.prohibit_duplicate_selection(self.ui.param_heat_map_2, self.ui.param_heat_map_1))
        self.ui.additional_graphics_btn.clicked.connect(self.draw_additional_graphics)
        self.ui.open_data_file_btn.clicked.connect(self.open_data_file)

    def add_linear_graph(self):
        algorithms = self.get_active_algorithm()
        # TODO: переименовать переменные, нихрена не понятно
        d = self.get_value_from_combobox(self.ui.param_linear_graph)
        if d == {None: ''}:
            error = "Выберите параметр итерирования"
            self.print_error(error)
            return
        p = AlgorithmParameter.get_parameters(list(d.keys())[0])
        print("Параметр для построения графика: ", list(d.keys())[0])
        n = self.ui.list_graph.count()
        if n > 0:
            self.ui.list_graph.takeAt(n - 1)
        if p.allowable_values is not None:
            point_graph = PossibleGraph("POINT_GRAPH", p, [], algorithms)
            point_graph_wdg = PointGraphWidget(point_graph)
            self.ui.list_graph.addWidget(point_graph_wdg.get_widget(parent=self, algorithms=algorithms,
                                                                    print_error=self.print_error))
        else:
            line_graph = PossibleGraph("LINE_GRAPH", p, [], [])
            line_graph_wdg = LineGraphWidget(line_graph)
            self.ui.list_graph.addWidget(line_graph_wdg.get_widget(lower_limit=0, top_limit=1000,
                                                                   step_limit=1, algorithms=algorithms,
                                                                   print_error=self.print_error))
        self.ui.list_graph.addStretch(1)

    def add_heat_map(self):
        algorithms = self.get_active_algorithm()
        param_x = self.get_value_from_combobox(self.ui.param_heat_map_1)
        param_y = self.get_value_from_combobox(self.ui.param_heat_map_2)
        if (param_x == param_y) or (param_x == {None: ''}) or (param_y == {None: ''}):
            error = "Параметры итерирования выбраны некорректно!"
            self.print_error(error)
            return
        print(algorithms)
        if len(algorithms) != 1:
            error = "Должен быть выбран один алгоритм!"
            self.print_error(error)
            return
        p_x = AlgorithmParameter.get_parameters(list(param_x.keys())[0])
        p_y = AlgorithmParameter.get_parameters(list(param_y.keys())[0])
        print("Параметр для построения графика: ", list(param_x.keys())[0], list(param_y.keys())[0])
        n = self.ui.list_graph.count()
        if n > 0:
            self.ui.list_graph.takeAt(n - 1)
        graph = PossibleGraph("HEAT_MAP", [p_x, p_y], [], self.to_test_list)
        graph_widget = HeatMapWidget(graph)
        self.ui.list_graph.addWidget(graph_widget.get_widget(lower_limit=0, top_limit=1000,
                                                             step_limit=1, algorithm=algorithms,
                                                             print_error=self.print_error))
        self.ui.list_graph.addStretch(1)

    def get_value_from_combobox(self, combobox):
        text = combobox.currentText()
        key = combobox.currentData()
        d = {key: text}
        print(d)
        return d

    def add_parameters_in_combobox(self, get_idx_active_cb):
        def f():
            """
            
            :return: 
            """
            idx_active_cb = get_idx_active_cb()
            params = self.get_params_on_idx(self.to_test_list, idx_active_cb)
            common_params = self.get_common_params(*params)
            print(common_params)
            self.param_in_combobox_for_heat_map = common_params
            self.fill_combobox(common_params,
                               self.ui.param_linear_graph,
                               self.ui.param_heat_map_1,
                               self.ui.param_heat_map_2)
        return f

    def get_params_on_idx(self, to_test_list, idx_list):
        d = []
        for i in idx_list:
            alg = to_test_list[i]
            if alg is not None:
                p = alg.get_params_dict()
                d.append(p)
        return d

    def get_params(self, to_test_list):
        d = []
        for alg in to_test_list:
            if alg is not None:
                p = alg.get_params_dict()
                d.append(p)
        return d

    def fill_combobox(self, data, *args):
        # TODO: перенести в общие
        for cmb in args:
            cmb.clear()
            for k in data.keys():
                if (k != "EC") and (k != "RN"):
                    cmb.addItem(data.get(k), k)

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

    def get_active_algorithm(self):
        idx = self.get_selected_algorithms()
        algorithms = [self.to_test_list[idx[i]] for i in range(len(idx))]
        return algorithms

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

        self.ui.add_row_in_form(self.ui.alg_form, a.get_parameters(), name, "Параметризировать", cb_handler, self)

    def prohibit_duplicate_selection(self, cmb, cmb1):
        item = cmb.currentText()
        item_data = cmb.currentData()

        item1 = cmb1.currentText()

        list_without_item = []
        cmb1.clear()
        for i in self.param_in_combobox_for_heat_map.keys():
            if item_data != i:
                list_without_item.append(i)
                cmb1.addItem(self.param_in_combobox_for_heat_map.get(i), i)

        if item != item1:
            cmb1.setCurrentText(item1)

    def print_error(self, text: str) -> None:
        """Вывод сообщения об ошибке на экран"""
        QMessageBox.information(self, 'Внимание!', text,
                                QMessageBox.Cancel, QMessageBox.Cancel)

    def draw_additional_graphics(self):
        flags = [g['draw'] for g in self.settings.additional_graphics]
        if not any(flags):
            error = "Не выбрано ни одного дополнительного графика"
            self.print_error(error)
            return
        algorithms = self.get_active_algorithm()
        test_func_data = read_json(self.settings.abs_path_test_func)
        all_data = []
        if not algorithms:
            error = "Не выбрано ни одного алгоритма"
            self.print_error(error)
            return
        if self.ui.data_path_le.text() != "":
            # TODO: здесь чтение данных из файла
            abs_path = self.ui.data_path_le.text()
            data = read_json(abs_path)
            all_data.append(data['runs'][0])
        else:
            script_path = os.path.dirname(os.path.abspath(__file__))
            for alg in algorithms:
                number_runs = alg.settings.number_of_runs
                alg.settings.number_of_runs = 1
                alg.write_parameters()
                file_name = alg.get_identifier_name() + '.json'
                abs_path = os.path.join(script_path, "..\\algorithms_exe\\result\\", file_name)
                print(abs_path)
                alg.run(abs_path, self.settings.abs_path_test_func)
                return_code, run_time = alg.wait_process()
                if return_code != 0:
                    self.print_error("Ошибка при работе алгоритма")
                    return
                data = read_json(abs_path)
                all_data.append(data['runs'][0])
                alg.settings.number_of_runs = number_runs
                alg.write_parameters()

        for g in self.settings.additional_graphics:
            if g['draw'] and g['name'] == "График движения лучшей точки":
                func = get_test_func(test_func_data['type'],
                                     test_func_data['number_extrema'], test_func_data['coefficients_abruptness'],
                                     test_func_data['coordinates'], test_func_data['degree_smoothness'],
                                     test_func_data['func_values'])
                last_iter = min(operator.getitem(i, 'stop_iteration') for i in all_data)
                stop_iter = g['iter'] if g['iter'] <= last_iter else last_iter
                data = [operator.getitem(d, 'coordinates')[:stop_iter] for d in all_data]
                motion_point_graph(data, func, lbl=[alg.get_identifier_name() for alg in algorithms],
                                   file_name="motion_graph.png", x_label="${x}{_0}$", y_label="${x}{_1}$",
                                   title=g['name'] + " за " + str(g['iter']) + " итераций")

            data = []
            max_stop_iter = max(operator.getitem(i, 'stop_iteration') for i in all_data)
            for d in all_data:
                meaningful_data = operator.getitem(d, g['name_field'])[:d['stop_iteration']]
                if d['stop_iteration'] < max_stop_iter:
                    data.append(
                        meaningful_data + [meaningful_data[-1] for _ in range(max_stop_iter - len(meaningful_data))])
                else:
                    data.append(meaningful_data)

            if g['draw'] and g['name'] == "График сходимости по координатам":
                graph_convergence_coord(data, [i for i in range(max_stop_iter)],
                                        lbl=[["${x}{_0}$", "${x}{_1}$"] for _ in range(len(algorithms))],
                                        file_name=["graph_convergence_coord_" + alg.get_identifier_name() + ".png" for alg in algorithms],
                                        x_label="${t}$", y_label="${x}$", title=g['name'], single_graph=False, marker=None)
            elif g['draw'] and g['name'] == "График сходимости по значениям функции":
                file_name = "graph_convergence_func_value_" + alg.get_name() + ".png"
                line_graph(data, [i for i in range(max_stop_iter)],
                           lbl=[alg.get_identifier_name() for alg in algorithms], file_name=file_name,
                           x_label="${t}$", y_label="${f(x)}$", title=g['name'], marker='')
            elif g['draw'] and g['name'] == "График дисперсии":  # переделать для дисперсии.
                data = np.array(data)
                dim = self.settings.dimension
                if data.shape[-1] != dim:
                    label = ["${\sigma}{_x}$_" + alg.get_name().replace(' ', '_') for _ in range(len(algorithms))]
                    file_name = "graph_dispersion_" + alg.get_identifier_name() + ".png"
                else:
                    label = [["${\sigma}{_x}{_" + str(i) + "}$" for i in range(dim)] for _ in range(len(algorithms))]
                    file_name = ["graph_dispersion_" + alg.get_identifier_name() + ".png" for alg in algorithms]
                graph_convergence_coord(data, [i for i in range(max_stop_iter)],
                                        lbl=label,
                                        file_name=file_name,
                                        x_label="${t}$", y_label="${\sigma}^2$", title=g['name'], single_graph=False)

        # TODO: определиться откуда брать данные? (или делать прогон отдельно, или брать из файла)
        # TODO: можно предложить открыть файл с данными и оттуда считать все.

    def open_data_file(self) -> None:
        """
        Метод открытия окна для выбора json-файла с данными для построения графиков.
        Обработчик события нажатия на кнопку self.ui.open_data_file_btn.
        :return: None.
        """
        file_name = open_file_dialog("Открыть json-файл данных",
                                     "All Files (*);;JSON Files (*.json)", self)
        if file_name:
            self.ui.data_path_le.setText(file_name)

    def open_about_dialog(self) -> None:
        """Метод открытия окна "О программе" """
        self.about = AboutDialog(flags=Q_FLAGS())
        self.about.show()
