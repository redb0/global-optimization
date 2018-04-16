import AlgorithmParameter
from algorithms.SAC import SAC


class StandardSAC(SAC):
    """Стандартный алгорит селективного усреднения координат (без модификаций)"""
    def __init__(self):
        super().__init__()
        self.name = "Standard SAC"
        self.full_name = "Метод селективного усреднения"
        # self._relative_path = "..\\algorithms_exe\\standard_sac.exe"  # пусть до exe-шника с алгоритмом на golang
        self.config_file = "..\\algorithms_exe\\standard_sac_config.json"
        self.result_file_name = "..\\algorithms_exe\\result\\standard_sac_res.json"

        self.parameters = [AlgorithmParameter.get_MI(), AlgorithmParameter.get_NP(), AlgorithmParameter.get_KN(),
                           AlgorithmParameter.get_gamma(), AlgorithmParameter.get_SF(), AlgorithmParameter.get_KQ(),
                           AlgorithmParameter.get_NF()]

    # def run(self, result_file_name: str, file_test_func: str) -> str:
    #     """
    #     Метод для запуска алгоритма.
    #
    #     :param file_test_func: json-файл с информацией о тестовой функции.
    #     :param result_file_name: имя файла в виде строки (*.json), куда будет сохранен результат.
    #     :return:
    #     """
    #     # os.path.dirname(__file__) - возвращает путь до папки, где лежит файл
    #     # os.path.realpath(__file__) - возвращает путь к файлу, вместе с его названием
    #     script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\\\', '\\')
    #     abs_path_exe = os.path.join(script_path, self._relative_path)  # путь до exe-шника
    #     abs_path_config = os.path.join(script_path, self.config_file)  # путь до конфиг файла
    #     abs_path_result = os.path.join(script_path, result_file_name)  # пусть куда положить результат
    #     if self._process is None:
    #         args = [abs_path_exe, abs_path_config, file_test_func, abs_path_result]
    #         # записать параметры алгоритма в файл config
    #         print(to_dict(self.parameters, min_flag=self.settings.min_flag))
    #         write_json(abs_path_config, to_dict(self.parameters,
    #                                             min_flag=self.settings.min_flag))
    #
    #         self._start_time = time()
    #         self._process = subprocess.Popen(args, shell=True,
    #                                          stdout=subprocess.PIPE)  # bufsize=1, universal_newlines=True
    #         print(self._process.pid)
    #         # TODO: получить вывод из процесса
    #         # TODO: возвратить из этой функции значение функции, координату, массив с лучшими значениями, массив с лучшими координатами
    #         return abs_path_result
    #     else:
    #         print("Уже запущен какой-то процесс")
    #         return ""

    # def find_probability_estimate(self, extremum: list, epsilon: Union[list, float, int],
    #                               file_test_func: str, number_runs=100, file_path="") -> float:
    #     # extremum - из тестовой функции
    #     # epsilon - из настроек
    #     # TODO: сделать epsilon всегда одинарным списком.
    #     if (type(epsilon) == float) or (type(epsilon) == int):
    #         number_successful_starts = 0
    #     elif type(epsilon) == list:
    #         number_successful_starts = []
    #         for _ in epsilon:
    #             number_successful_starts.append(0)
    #
    #     # TODO: добавить возможность в настройках указывать путь до папки куда сохранять верузльтат
    #     script_path = os.path.dirname(os.path.abspath(__file__))
    #     script_path = script_path.replace('\\\\', '\\')
    #     name_file = self.get_identifier_name() + ".json"  # "StandardSAC_MI=500_NP=100_KN=0.0_SF=1.0_NF=1.json"
    #     abs_path_file = os.path.join(script_path, "..\\algorithms_exe\\result\\", name_file)  #
    #     print(name_file)
    #     in_file = []
    #     for i in range(number_runs):
    #         print("Прогон ", i + 1, " ...")
    #         path_res = self.run(self.result_file_name, file_test_func)  # TODO: доделать здесь
    #         t = self.wait_process()
    #         print(t)
    #         res_dict = read_json(path_res)
    #
    #         in_file.append(res_dict)
    #         x_best = res_dict["x_best"]
    #         if (type(epsilon) == float) or (type(epsilon) == int):
    #             mask = [lies_in_epsilon(x_best[k], extremum[k], epsilon) for k in range(len(x_best))]
    #             if all(mask):
    #                 number_successful_starts = number_successful_starts + 1
    #         elif type(epsilon) == list:
    #             for j in range(len(epsilon)):
    #                 mask = [lies_in_epsilon(x_best[k], extremum[k], epsilon[j]) for k in range(len(x_best))]
    #                 if all(mask):
    #                     number_successful_starts[j] = number_successful_starts[j] + 1
    #     write_json(abs_path_file, in_file)
    #
    #     return number_successful_starts / number_runs

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
