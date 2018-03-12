import os
import subprocess

from algorithms.GSA import GSA
import alg_parameters
from support_func import write_json


class StandardGSA(GSA):
    def __init__(self):
        super().__init__()
        self.name = "Standard GSA"
        self.full_name = "Гравитационный поиск"

        self._relative_path = "..\\algorithms_ex\\standard_gsa.exe"  # пусть до exe-шника с алгоритмом на golang
        self.config_file = "..\\algorithms_exe\\standard_gsa_config.json"
        self.process = None

        # TODO: возможно тут нужен кортеж как неизменяемый тип
        self.parameters = [alg_parameters.get_MI(), alg_parameters.get_NP(), alg_parameters.get_KN(),
                           alg_parameters.get_IG(), alg_parameters.get_G0(), alg_parameters.get_AG(),
                           alg_parameters.get_EC(), alg_parameters.get_RN(), alg_parameters.get_RP()]

    # def get_param_obj(self, key):
    #     for p in self.parameters:
    #         if key == p.abbreviation:
    #             return p

    def run(self, params: dict, result_file_name: str):
        """
        Метод для запуска алгоритма.
        
        :param params: 
        :param result_file_name: имя файла в виде строки (*.json), куда будет сохранен результат
        :return: 
        """

        script_path = os.path.dirname(os.path.abspath(__file__))  # os.path.realpath(__file__)
        script_path = script_path.replace('\\\\', '\\')
        print(script_path)
        abs_path_exe = os.path.join(script_path, self._relative_path)  # путь до exe-шника
        abs_path_config = os.path.join(script_path, self.config_file)  # путь до конфиг файла
        abs_path_result = os.path.join(script_path, "result\\" + result_file_name)  # пусть куда положить результат
        print(abs_path_exe)
        print(abs_path_config)
        print(abs_path_result)

        # print(os.path.dirname(os.path.abspath(__file__)))
        args = [abs_path_exe, abs_path_config, abs_path_result]
        # записать параметры алгоритма в файл config
        write_json(abs_path_config, params)  # запись параметров в json файл. может написать тут или во внешней функции?

        # self.process = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
        # TODO: получить вывод из процесса

    def wait(self):
        if self.process is not None:
            code = self.process.wait()
            return code

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
