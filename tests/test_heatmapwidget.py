import contextlib
import unittest
from unittest.mock import patch

import sys

import pytest
from PyQt5.QtWidgets import QApplication, QSpinBox, QDoubleSpinBox, QPushButton

from AlgorithmParameter import get_NF, get_ILCNP, get_KN, get_NP, get_MI, get_G0
from graph.HeatMap import HeatMap
from graph.PossibleGraph import PossibleGraph
from gui.mainwindow import MainWindow
from gui.wdg.HeatMapWidget import HeatMapWidget
from gui.wdg.RangeWidget import RangeWidget
from gui.wdg.SelectionWidget import SelectionWidget


class Closeable:
    def close(self):
        print('closed')


params = [([get_ILCNP(), get_NF()], [SelectionWidget, SelectionWidget]),
          ([get_NF(), get_MI()], [SelectionWidget, RangeWidget]),
          ([get_G0(), get_ILCNP()], [RangeWidget, SelectionWidget]),
          ([get_KN(), get_NP()], [RangeWidget, RangeWidget])
          ]


@pytest.fixture(params=params)
def param_loop(request):
    return request.param


class TestHeatMapWidget:
    def setup(self):
        self.app = QApplication(sys.argv)
        self.mw = MainWindow()
        self.mw.show()

    def teardown(self):
        with pytest.raises(SystemExit):
            with contextlib.closing(Closeable()):
                sys.exit()

    @patch.object(HeatMap, 'plot')
    @patch.object(HeatMap, '__init__')
    def test_plot_choose_param(self, no_init, no_plot):
        p_x = get_NF()  # [1, 2, 3, 4]
        p_y = get_ILCNP()  # [1, 2, 3, 4, 5, 6, 7]
        p_x.set_selected_values(1)
        p_y.set_selected_values(1)
        param = [p_x, p_y]

        obj = PossibleGraph("HEAT_MAP", param, [], [])

        wdg = HeatMapWidget(obj)
        wdg.selected_value = [[1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7]]

        no_init.return_value = None

        wdg.create_graph(lambda text: print(text), [])

        assert no_init.call_count == 1

        args = list(no_init.call_args_list[0])[0]
        assert wdg.selected_value == args[-1]

        assert no_plot.call_count == 1, "метод heat_map.plot не был вызван"

    @patch.object(HeatMap, 'plot')
    @patch.object(HeatMap, '__init__')
    @patch.object(QSpinBox, 'value')
    @patch.object(QDoubleSpinBox, 'value')
    def test_plot_input_param(self, no_double_value, no_int_value, no_init, no_plot):
        p_x = get_KN()  # 0.0, 10.0, 1.0
        p_y = get_NP()  # 100, 500, 100
        param = [p_x, p_y]

        def f():
            for i in [0.0, 10.0, 1.0]:
                yield i
            return None

        def f1():
            for i in [100, 500, 100]:
                yield i
            return None

        x = f()
        y = f1()

        no_int_value.side_effect = y.__next__
        no_double_value.side_effect = x.__next__
        no_init.return_value = None

        obj = PossibleGraph("HEAT_MAP", param, [], [])

        wdg = HeatMapWidget(obj)
        w = wdg.get_widget()

        expected_axis = [[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], [100, 200, 300, 400, 500]]

        wdg.create_graph(lambda text: print(text), [])

        assert no_init.call_count == 1

        args = list(no_init.call_args_list[0])[0]
        assert expected_axis == args[-1]

        assert no_plot.call_count == 1, "метод heat_map.plot не был вызван"

    def test_get_widget(self, param_loop):
        param, expected_type = param_loop
        obj = PossibleGraph("HEAT_MAP", param, [], [])
        wdg = HeatMapWidget(obj)
        w = wdg.get_widget()

        numb_btn = 0

        j = 0
        for i in range(wdg.grid.count()):
            item = wdg.grid.itemAt(i).widget()
            if type(item) == QPushButton:
                numb_btn += 1
            elif type(item) in expected_type:
                assert type(item) == expected_type[j]
                j += 1

        assert numb_btn == 2


if __name__ == '__main__':
    unittest.main()
