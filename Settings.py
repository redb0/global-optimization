import json
import os

from typing import Union, List

from Parameter import Parameter


class Settings:
    # TODO: добавить путь до папки куда сохранять результаты вычислений в json.
    _min_flag = Parameter("Тип задачи (1 - минимизация, 0 - максимизация)", int, 1, allowable_values=[0, 1])
    _number_of_runs = Parameter("Количество пусков алгоритма", int, 100)
    _epsilon = Parameter("Размер epsilon-окрестности", [float, list], 0.5)
    _abs_path_test_func = Parameter("Тестовая функция", str, "")  # путь до файла с тестовой функцийей
    _real_extrema = Parameter("Координаты глобального экстремума", list, [0, 0])
    _legend_position = Parameter("Положение легенда на графике", str, "top",
                                 allowable_values=["top", "left", "bottom", "right"])

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
            if all([((type(value[i]) == int) or (type(value[i] == float)) for i in range(len(value)))]):
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
                    data = json.load(f)
                self.__class__._real_extrema.present_value = data['real_extrema']
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
    def real_extrema(self) -> List[Union[int, float]]:
        return self.__class__._real_extrema.present_value

    # @real_extrema.setter
    # def real_extrema(self, value: List[Union[int, float]]):
    #     if self.__class__._abs_path_test_func.present_value != "":
    #         with open(self.__class__._abs_path_test_func.present_value, 'r', encoding='utf-8') as f:
    #             data = json.load(f)


def set_all_default_values(cls):
    print('------------------------')
    print(Settings._min_flag.present_value)
    print(Settings._epsilon.present_value)
    print(Settings._abs_path_test_func.present_value)
    print(Settings._legend_position.present_value)
    print(Settings._number_of_runs.present_value)
    d = cls.__dict__
    for p in d.keys():
        obj = d.get(p)
        if type(obj) == Parameter:
            obj.set_default_value()
    print('------------------------')
    print(Settings._min_flag.present_value)
    print(Settings._epsilon.present_value)
    print(Settings._abs_path_test_func.present_value)
    print(Settings._legend_position.present_value)
    print(Settings._number_of_runs.present_value)


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
