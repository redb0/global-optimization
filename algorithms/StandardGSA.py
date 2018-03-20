import json
import os
import subprocess
from time import time
from typing import Union

from algorithms.GSA import GSA
import alg_parameters
from support_func import write_json


class StandardGSA(GSA):
    def __init__(self):
        super().__init__()
        self.name = "Standard GSA"
        self.full_name = "Гравитационный поиск"

        self._relative_path = "..\\algorithms_exe\\StandardGSA.exe"  # пусть до exe-шника с алгоритмом на golang
        self.config_file = "..\\algorithms_exe\\standard_gsa_config.json"
        self.result_file_name = "..\\algorithms_exe\\result\\standard_gsa_res.json"
        self._process = None
        self._start_time = None

        # TODO: возможно тут нужен кортеж как неизменяемый тип
        self.parameters = [alg_parameters.get_MI(), alg_parameters.get_NP(), alg_parameters.get_KN(),
                           alg_parameters.get_IG(), alg_parameters.get_G0(), alg_parameters.get_AG(),
                           alg_parameters.get_EC(), alg_parameters.get_RN(), alg_parameters.get_RP(),
                           alg_parameters.get_gamma()]

    # def get_param_obj(self, key):
    #     for p in self.parameters:
    #         if key == p.abbreviation:
    #             return p

    def run(self, result_file_name: str, file_test_func: str):
        """
        Метод для запуска алгоритма.
        
        :param file_test_func: 
        :param params: 
        :param result_file_name: имя файла в виде строки (*.json), куда будет сохранен результат
        :return: 
        """
        # os.path.dirname(__file__) - возвращает путь до папки, где лежит файл
        # os.path.realpath(__file__) - возвращает путь к файлу, вместе с его названием
        script_path = os.path.dirname(os.path.abspath(__file__))
        script_path = script_path.replace('\\\\', '\\')
        # print(script_path)
        abs_path_exe = os.path.join(script_path, self._relative_path)  # путь до exe-шника
        abs_path_config = os.path.join(script_path, self.config_file)  # путь до конфиг файла
        abs_path_result = os.path.join(script_path, result_file_name)  # пусть куда положить результат
        # print(abs_path_exe)
        # print(abs_path_config)
        # print(abs_path_result)
        if self._process is None:
            args = [abs_path_exe, abs_path_config, file_test_func, abs_path_result]
            # записать параметры алгоритма в файл config
            print(self.get_params_dict_2(min_flag=1))
            write_json(abs_path_config, self.get_params_dict_2(min_flag=1))  # может написать тут или во внешней функции?

            self._start_time = time()
            self._process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)  # bufsize=1, universal_newlines=True
            print(self._process.pid)
            # TODO: получить вывод из процесса
            # TODO: возвратить из этой функции значение функции, координату, массив с лучшими значениями, массив с лучшими координатами
            return abs_path_result
        else:
            print("Уже запущен какой-то процесс")

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

    def get_result(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def find_probability_estimate(self, extremum: list, epsilon: Union[list, float, int], file_test_func: str, number_runs=100):
        # number_successful_starts = 0
        if (type(epsilon) == float) or (type(epsilon) == int):
            number_successful_starts = 0
        elif type(epsilon) == list:
            number_successful_starts = []
            for _ in epsilon:
                number_successful_starts.append(0)

        for i in range(number_runs):
            print("Прогон ", i + 1, " ...")
            path_res = self.run(self.result_file_name, file_test_func)  #TODO: доделать здесь
            t = self.wait_process()
            print(t)
            # func_value, coordinate, best_func_value, best_coordinates = res
            res_dict = self.get_result(path_res)
            print(res_dict)
            if (type(epsilon) == float) or (type(epsilon) == int):
                mask = [self.lies_in_epsilon(res_dict["x_best"][k], extremum[k], epsilon) for k in range(len(res_dict["x_best"]))]
                if all(mask):
                    number_successful_starts = number_successful_starts + 1
            elif type(epsilon) == list:
                for j in range(len(epsilon)):
                    mask = [self.lies_in_epsilon(res_dict["x_best"][k], extremum[k], epsilon[j]) for k in range(len(res_dict["x_best"]))]
                    if all(mask):
                        number_successful_starts[j] = number_successful_starts[j] + 1
        return number_successful_starts

    def lies_in_interval(self, x, left, right):
        if (x >= left) and (x <= right):
            return True
        return False

    def lies_in_epsilon(self, x, c, e):
        if (x >= (c - e)) and (x <= (c + e)):
            return True
        return False

    def get_abbreviation_params(self):
        # abr = {i.get_abbreviation() for i in self.parameters}
        abr = [i.get_abbreviation() for i in self.parameters]
        return abr

    def get_description_param(self, abr: str) -> str:
        for p in self.parameters:
            if abr == p.abbreviation:
                return p.name

    def get_params_dict(self):
        d = {}
        for p in self.parameters:
            d.update({p.abbreviation: p.name})
        return d

    def get_params_dict_2(self, **kwargs):
        d = {}
        for p in self.parameters:
            d.update({p.abbreviation: p.selected_values})
        for name in kwargs.keys():
            d.update({name: kwargs.get(name)})
        return d

    def set_params_value(self, list_p, **kwargs):
        """
        
        :param list_p: 
        :param kwargs: 
        :return: 
        """
        for k in kwargs.keys():
            obj = alg_parameters.get_param_from_list(list_p, k)
            if obj is not None:
                obj.set_selected_values(kwargs.get(k))
            else:
                print("Параметра не существует")

    # def get_parameters(self):
    #     return self.parameters


def main():
    s = StandardGSA()
    x = s.get_abbreviation_params()
    print(x)
    x1 = alg_parameters.Parameters.get_list_key(s.get_parameters())
    print(x1)
    res = "res.json"
    d = {'MI': 1, 'NP': 2, 'KN': 3, 'IG': 4, 'G0': 5, 'AG': 6, 'EC': 7, 'RN': 8, 'RP': 10}
    s.run(d, res)


if __name__ == '__main__':
    main()
