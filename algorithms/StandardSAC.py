import AlgorithmParameter
from algorithms.SAC import SAC


class StandardSAC(SAC):
    """Стандартный алгорит селективного усреднения координат (без модификаций).
    Algorithm Selective Averaging Coordinates (SAC).
    Подробнее (more information):
    http://sun.tsu.ru/mminfo/000063105/inf/22/image/22-114.pdf
    """
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
