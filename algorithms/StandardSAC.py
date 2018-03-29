import os
import subprocess
from time import time
from typing import Union

import AlgorithmParameter
from Settings import Settings
from algorithms.SAC import SAC
from support_func import to_dict, write_json, read_json, lies_in_epsilon


class StandardSAC(SAC):
    """Стандартный алгорит селективного усреднения координат (без модификаций)"""
    def __init__(self):
        super().__init__()
        self.name = "Standard SAC"
        self.full_name = "Метод селективного усреднения"
        self._relative_path = "..\\algorithms_exe\\standard_sac.exe"  # пусть до exe-шника с алгоритмом на golang
        self.config_file = "..\\algorithms_exe\\standard_sac_config.json"
        self.result_file_name = "..\\algorithms_exe\\result\\standard_sac_res.json"
        self._process = None
        self._start_time = None

        self.parameters = [AlgorithmParameter.get_MI(), AlgorithmParameter.get_NP(), AlgorithmParameter.get_KN(),
                           AlgorithmParameter.get_gamma(), AlgorithmParameter.get_SF(), AlgorithmParameter.get_KQ(),
                           AlgorithmParameter.get_NF()]

        self.settings = Settings()

    def get_params_dict(self):
        d = {}
        for p in self.parameters:
            d.update({p.abbreviation: p.name})
        return d

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
        abs_path_exe = os.path.join(script_path, self._relative_path)  # путь до exe-шника
        abs_path_config = os.path.join(script_path, self.config_file)  # путь до конфиг файла
        abs_path_result = os.path.join(script_path, result_file_name)  # пусть куда положить результат
        if self._process is None:
            args = [abs_path_exe, abs_path_config, file_test_func, abs_path_result]
            # записать параметры алгоритма в файл config
            print(to_dict(self.parameters, min_flag=self.settings.min_flag))
            write_json(abs_path_config, to_dict(self.parameters,
                                                min_flag=self.settings.min_flag))

            self._start_time = time()
            self._process = subprocess.Popen(args, shell=True,
                                             stdout=subprocess.PIPE)  # bufsize=1, universal_newlines=True
            print(self._process.pid)
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
        # TODO: сделать epsilon всегда одинарным списком.
        if (type(epsilon) == float) or (type(epsilon) == int):
            number_successful_starts = 0
        elif type(epsilon) == list:
            number_successful_starts = []
            for _ in epsilon:
                number_successful_starts.append(0)

        # TODO: добавить возможность в настройках указывать путь до папки куда сохранять верузльтат
        script_path = os.path.dirname(os.path.abspath(__file__))
        script_path = script_path.replace('\\\\', '\\')
        name_file = (self.name.replace(' ', '') + "_" +
                     self.parameters[0].get_abbreviation() + "=" + str(self.parameters[0].get_selected_values()) + "_" +
                     self.parameters[1].get_abbreviation() + "=" + str(self.parameters[1].get_selected_values()) + "_" +
                     self.parameters[2].get_abbreviation() + "=" + str(self.parameters[2].get_selected_values()) + "_" +
                     self.parameters[4].get_abbreviation() + "=" + str(self.parameters[4].get_selected_values()) + "_" +
                     self.parameters[6].get_abbreviation() + "=" + str(self.parameters[6].get_selected_values()) +
                     ".json")  # "StandardSAC_MI=500_NP=100_KN=0.0_SF=1.0_NF=1.json"
        abs_path_file = os.path.join(script_path, "..\\algorithms_exe\\result\\", name_file)  #
        print(name_file)
        in_file = []
        for i in range(number_runs):
            print("Прогон ", i + 1, " ...")
            path_res = self.run(self.result_file_name, file_test_func)  # TODO: доделать здесь
            t = self.wait_process()
            print(t)
            res_dict = read_json(path_res)

            in_file.append(res_dict)
            x_best = res_dict["x_best"]
            if (type(epsilon) == float) or (type(epsilon) == int):
                mask = [lies_in_epsilon(x_best[k], extremum[k], epsilon) for k in range(len(x_best))]
                if all(mask):
                    number_successful_starts = number_successful_starts + 1
            elif type(epsilon) == list:
                for j in range(len(epsilon)):
                    mask = [lies_in_epsilon(x_best[k], extremum[k], epsilon[j]) for k in range(len(x_best))]
                    if all(mask):
                        number_successful_starts[j] = number_successful_starts[j] + 1
        write_json(abs_path_file, in_file)

        return number_successful_starts / number_runs

    def get_abbreviation_params(self):
        abr = [i.get_abbreviation() for i in self.parameters]
        return abr

    def get_description_param(self, abr: str) -> str:
        for p in self.parameters:
            if abr == p.abbreviation:
                return p.name

    def get_value_param_on_abbreviation(self, abr: str):
        for p in self.parameters:
            if abr == p.abbreviation:
                return p.get_selected_values()

    def set_params_value(self, list_p, **kwargs):
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

    def get_identifier_name(self) -> str:
        """
        Метод построения уникального имени. Для использования в качестве имени файла или подписи к графику.
        Имя складывается из сокращенного названия алгоритма и его параметров.
        :return: имя в виде строки. Напримен "s_sac_MI=500_NP=200_KN=0.0_"
        """
        name = ("s_sac_" +
                self.parameters[0].get_abbreviation() + "=" + str(self.parameters[0].get_selected_values()) + "_" +
                self.parameters[1].get_abbreviation() + "=" + str(self.parameters[1].get_selected_values()) + "_" +
                self.parameters[2].get_abbreviation() + "=" + str(self.parameters[2].get_selected_values()) + "_" +
                self.parameters[4].get_abbreviation() + "=" + str(self.parameters[4].get_selected_values()) + "_" +
                self.parameters[6].get_abbreviation() + "=" + str(self.parameters[6].get_selected_values()) + "_" +
                self.parameters[3].get_abbreviation() + "=" + str(self.parameters[3].get_selected_values()) + "_" +
                self.parameters[5].get_abbreviation() + "=" + str(self.parameters[5].get_selected_values()))
        return name
