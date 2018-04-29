import json
import os

from typing import Union, List

from Parameter import Parameter


class Settings:
    # TODO: добавить путь до папки куда сохранять результаты вычислений в json.
    # TODO: добавить считывание реального экстремума и окно для него в настройках
    # TODO: добавить поле для установки размера шрифта на графике
    _min_flag = Parameter("Тип задачи (1 - минимизация, 0 - максимизация)", int, 1, allowable_values=[0, 1])
    _number_of_runs = Parameter("Количество пусков алгоритма", int, 100)
    _epsilon = Parameter("Размер epsilon-окрестности", [float, list], 0.5)
    _abs_path_test_func = Parameter("Тестовая функция", str, "")  # путь до файла с тестовой функцийей
    _global_min = Parameter("Координаты глобального минимума", list, [0, 0])
    _global_max = Parameter("Координаты глобального максимума", list, [0, 0])
    _legend_position = Parameter("Положение легенда на графике", str, "top",
                                 allowable_values=["top", "left", "bottom", "right"])
    _dimension = Parameter("Размерность задачи", int, 0)

    _report = True  # отчет json, в настройках сделать галочку "составлять для всех прогонов" и "не составлять"
    # [
    #   "time": {"min": 0, "mean": 0, "max": 0},
    #   "iteration": {"min": 0, "mean": 0, "max": 0}
    # ]
    # Дополнительные графики, сделать для них галочку "название графика" \/
    # _draw_convergence_func_value = True  # сходимость по значениям функции, по X - номер итерации, по Y - значения функции
    # _draw_convergence_coordinates = True  # сходимость по координатам, по X - номер итерации, по Y - координата
    # _draw_dispersion_graph = True  # график дисперсии
    # _draw_graph_best_point_motion = True  # график движения лучшей точки
    # _draw_graph_number_iteration = False  # ??? точечный график количества итераций, по X - номер прогона, по Y - количество итераций

    _additional_graphics = [{'name': "График сходимости по значениям функции", 'draw': True},
                            {'name': "График сходимости по координатам", 'draw': True},
                            {'name': "График движения лучшей точки", 'draw': True},
                            {'name': "График дисперсии", 'draw': True},
                            {'name': "График количества рабочих итераций", 'draw': False}]

    def __init__(self):
        pass

    @property
    def min_flag(self) -> int:
        return self.__class__._min_flag.present_value

    @min_flag.setter
    def min_flag(self, value: int) -> None:
        if value in self.__class__._min_flag.allowable_values:
            self.__class__._min_flag.present_value = value
        else:
            print("Недопустимое значения флага минимизации. Установлено значение по умолчанию (1)")
            self.__class__._min_flag.set_default_value()

    @property
    def number_of_runs(self) -> int:
        return self.__class__._number_of_runs.present_value

    @number_of_runs.setter
    def number_of_runs(self, value: int) -> None:
        if value > 0:
            self.__class__._number_of_runs.present_value = value
        else:
            print("Количество прогонов должно быть больше 0. Установлено значение по умолчанию (100).")
            self.__class__._number_of_runs.set_default_value()

    @property
    def epsilon(self) -> Union[float, int, List[Union[int, float]]]:
        return self.__class__._epsilon.present_value

    @epsilon.setter
    def epsilon(self, value: Union[float, int, List[Union[int, float]]]) -> None:
        if (type(value) == int) or (type(value) == float):
            if value > 0:
                self.__class__._epsilon.present_value = value
            else:
                print("Epsilon должно быть больше 0. Установлено значение по умолчанию (0.5).")
                self.__class__._epsilon.set_default_value()
        elif type(value) == list:
            if all([(type(value[i]) == int) or (type(value[i]) == float) for i in range(len(value))]):
                self.__class__._epsilon.present_value = value
            else:
                print("Недопустимый тип epsilon.")
                self.__class__._epsilon.set_default_value()
        else:
            print("Недопустимый тип epsilon.")
            self.__class__._epsilon.set_default_value()

    @property
    def abs_path_test_func(self) -> str:
        return self.__class__._abs_path_test_func.present_value

    @abs_path_test_func.setter
    def abs_path_test_func(self, value: str) -> None:
        if value == "":
            print("Не указано расположение файла тестовой функции.")
            self.__class__._abs_path_test_func.set_default_value()
        else:
            if os.path.isfile(value):
                self.__class__._abs_path_test_func.present_value = value
                with open(self.__class__._abs_path_test_func.present_value, 'r', encoding='utf-8') as f:
                    try:
                        json.load(f)
                        # self.__class__._global_min.present_value = data['real_extrema']
                    except UnicodeDecodeError:
                        print("Передан не json файл.")
                        self.__class__._abs_path_test_func.set_default_value()
            else:
                print("Значение не является путем.")
                self.__class__._abs_path_test_func.set_default_value()

    @property
    def legend_position(self) -> str:
        return self.__class__._legend_position.present_value

    @legend_position.setter
    def legend_position(self, value: str) -> None:
        if value in self.__class__._legend_position.allowable_values:
            self.__class__._legend_position.present_value = value
        else:
            print("Некорректное расположение легенды. Установлено значение по умолчанию (top)")
            self.__class__._legend_position.set_default_value()

    @property
    def global_min(self) -> List[Union[int, float]]:
        return self.__class__._global_min.present_value

    @global_min.setter
    def global_min(self, value: List[Union[int, float]]) -> None:
        if type(value) == list:
            self.__class__._global_min.present_value = value
        else:
            self.__class__._global_min.set_default_value()

    @property
    def global_max(self) -> List[Union[int, float]]:
        return self.__class__._global_max.present_value

    @global_max.setter
    def global_max(self, value: List[Union[int, float]]) -> None:
        if type(value) == list:
            self.__class__._global_max.present_value = value
        else:
            self.__class__._global_max.set_default_value()

    @property
    def dimension(self) -> int:
        return self.__class__._dimension.present_value

    @dimension.setter
    def dimension(self, value: int) -> None:
        self.__class__._dimension.present_value = value

    @property
    def draw_con_coord(self):
        return self.__class__._additional_graphics[1]

    @draw_con_coord.setter
    def draw_con_coord(self, value: bool) -> None:
        self.__class__._additional_graphics[1]['draw'] = value

    @property
    def draw_con_func_value(self):
        return self.__class__._additional_graphics[0]

    @draw_con_func_value.setter
    def draw_con_func_value(self, value: bool) -> None:
        self.__class__._additional_graphics[0]['draw'] = value

    @property
    def draw_point_motion(self):
        return self.__class__._additional_graphics[2]

    @draw_point_motion.setter
    def draw_point_motion(self, value: bool) -> None:
        self.__class__._additional_graphics[2]['draw'] = value

    @property
    def draw_dispersion_graph(self):
        return self.__class__._additional_graphics[3]

    @draw_dispersion_graph.setter
    def draw_dispersion_graph(self, value: bool) -> None:
        self.__class__._additional_graphics[3]['draw'] = value

    @property
    def draw_graph_number_iteration(self):
        return self.__class__._additional_graphics[4]

    @draw_graph_number_iteration.setter
    def draw_graph_number_iteration(self, value: bool) -> None:
        self.__class__._additional_graphics[4]['draw'] = value

    @property
    def additional_graphics(self):
        return self.__class__._additional_graphics


def set_all_default_values(cls):
    d = cls.__dict__
    for p in d.keys():
        obj = d.get(p)
        if type(obj) == Parameter:
            obj.set_default_value()


def get_attributes(cls):
    """
    Метод возвращает все атрибуты (настройки) класса.
    :return: словарь (dict) с полями
    """
    d = cls.__dict__
    print(d)
    parameters = {}
    for p in d.keys():
        if type(d.get(p)) == Parameter:
            parameters.update({p: d.get(p)})
    print(parameters)
    return parameters
