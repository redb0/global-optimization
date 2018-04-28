import os
from time import time
import subprocess

from typing import List, Union

import AlgorithmParameter
from Settings import Settings

from support_func import to_dict, write_json, read_json


class Algorithm:
    def __init__(self):
        self.class_alg = ""
        self.name = ""
        self.full_name = ""
        self._exe_relative_path = "..\\algorithms_exe\\algorithms.exe"
        self.result_file_name = ""
        self.config_file = ""
        self.parameters = None
        self._start_time = None
        self._process = None

        self.settings = Settings()

    def get_class(self) -> str:
        return self.class_alg

    def get_name(self) -> str:
        return self.name

    def get_full_name(self):
        return self.full_name

    def get_parameters(self):
        return self.parameters

    def get_identifier_name(self) -> str:
        """Метод генерации уникального имени"""
        pass

    def get_abbreviation_params(self) -> List[str]:
        """Метод получения списка аббревиатур параметров алгоритма"""
        abr = [i.get_abbreviation() for i in self.parameters]
        return abr

    def get_description_param(self, abr: str) -> str:
        """Метод возвращает полное название параметра по его аббревиатуре"""
        for p in self.parameters:
            if abr == p.abbreviation:
                return p.name

    def get_value_param_on_abbreviation(self, abr: str):
        """Метод возвращает значение параметра алгоритма по его аббревиатуре"""
        for p in self.parameters:
            if abr == p.abbreviation:
                return p.get_selected_values()

    def set_parameter(self, key: str, value) -> None:
        """
        Метод для установки значения параметра по сокращенному обозначению.
        :param key: сокращенное обозначение параметра в виде строки
        :param value: значение
        :return: -
        """
        for p in self.parameters:
            if p.get_abbreviation() == key:
                p.set_selected_values(value)

    def set_params_value(self, list_p, **kwargs):
        # TODO: нигде не используется
        """

        :param list_p: 
        :param kwargs: 
        :return: 
        """
        for k in kwargs.keys():
            obj = AlgorithmParameter.get_param_from_list(list_p, k)
            if obj is not None:
                obj.set_selected_values(kwargs.get(k))
            else:
                print("Параметра не существует")

    def get_params_dict(self) -> dict:
        """
        Метод преобразует список параметров в словарь 
        с ключами - сокращенным обозначением и значениями - полным названием параметра
        :return: словарь
        """
        d = {}
        for p in self.parameters:
            d.update({p.abbreviation: p.name})
        return d

    def write_parameters(self):
        script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\\\', '\\')
        abs_path_config = os.path.join(script_path, self.config_file)  # путь до конфиг файла

        if type(self.settings.epsilon) in [int, float]:
            epsilon = [self.settings.epsilon for i in range(len(self.settings.dimension))]
        elif type(self.settings.epsilon) is list:
            epsilon = self.settings.epsilon
        else:
            print("Некорректно указана epsilon-окрестность")
            return

        print(to_dict(self.parameters, min_flag=self.settings.min_flag,
                      epsilon=epsilon, number_runs=self.settings.number_of_runs))
        write_json(abs_path_config, to_dict(self.parameters, min_flag=self.settings.min_flag,
                                            epsilon=epsilon, number_runs=self.settings.number_of_runs))

    def run(self, result_file_name: str, file_test_func: str) -> str:
        """
        Метод для запуска алгоритма.

        :param file_test_func: json-файл с информацией о тестовой функции.
        :param result_file_name: имя файла в виде строки (*.json), куда будет сохранен результат.
        :return: 
        """
        # os.path.dirname(__file__) - возвращает путь до папки, где лежит файл
        # os.path.realpath(__file__) - возвращает путь к файлу, вместе с его названием
        script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\\\', '\\')
        abs_path_exe = os.path.join(script_path, self._exe_relative_path)  # путь до exe-шника
        abs_path_config = os.path.join(script_path, self.config_file)  # путь до конфиг файла
        abs_path_result = os.path.join(script_path, result_file_name)  # пусть куда положить результат
        if self._process is None:
            args = [abs_path_exe, self.name.replace(' ', ''), abs_path_config, file_test_func, abs_path_result]

            self._start_time = time()
            self._process = subprocess.Popen(args, shell=True,
                                             stdout=subprocess.PIPE)  # bufsize=1, universal_newlines=True
            # print(self._process.pid)
            # TODO: получить вывод из процесса
            # TODO: возвратить из этой функции значение функции, координату, массив с лучшими значениями, массив с лучшими координатами
            return abs_path_result
        else:
            print("Уже запущен какой-то процесс")
            return ""

    def wait_process(self):
        """
        Метод ожидания окончания процесса работы алгоритма.
        :return: return_code: код завершения процесса
        :return: run_time   : время работы процесса в секундах
        """
        if self._process is not None:
            return_code = self._process.wait()
            end_time = time()
            run_time = end_time - self._start_time
            self._process = None  # сбросить процесс, так как он завершен
            return return_code, run_time

    def find_probability_estimate(self, extremum: list, epsilon: Union[list, float, int],
                                  file_test_func: str, number_runs=100, file_path="") -> float:
        # extremum - из тестовой функции
        # epsilon - из настроек

        # TODO: добавить возможность в настройках указывать путь до папки куда сохранять верузльтат
        script_path = os.path.dirname(os.path.abspath(__file__))
        script_path = script_path.replace('\\\\', '\\')
        name_file = self.get_identifier_name() + ".json"  # "s_gsa_MI=500_NP=100_KN=0.0_IG=1.json"
        abs_path_file = os.path.join(script_path, "..\\algorithms_exe\\result\\", name_file)  #
        print(name_file)

        self.write_parameters()

        self.result_file_name = abs_path_file

        abs_path_result = self.run(self.result_file_name, file_test_func)
        if abs_path_result == "":
            print("Что-то пошло не так!")
            return -1

        return_code, run_time = self.wait_process()
        print("Код завершения go-процесса ", return_code)
        print("Суммарное время прогонов ", run_time)

        res = read_json(abs_path_result)
        print("Оценка вероятности ", res["probability"])
        print(res["runs"])

        return res["probability"]

    # def get_name_params(self) -> List[str]:
    #     return list(self.parameters.values())

    # def get_keys_params(self) -> List[str]:
    #     return list(self.parameters.keys())
