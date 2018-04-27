from algorithms.GSA import GSA
import AlgorithmParameter


class StandardGSA(GSA):
    """Стандартный алгоритм гравитационного поиска (без модификаций).
    Gravitation Search Algorithm (GSA).
    Подробнее (more information):
    http://ahmetcevahircinar.com.tr/wp-content/uploads/2017/04/GSA_A_Gravitational_Search_Algorithm.pdf
    """
    def __init__(self):
        super().__init__()
        self.name = "Standard GSA"
        self.full_name = "Гравитационный поиск"

        # self._relative_path = "..\\algorithms_exe\\standard_gsa.exe"  # пусть до exe-шника с алгоритмом на golang
        self.config_file = "..\\algorithms_exe\\standard_gsa_config.json"
        self.result_file_name = "..\\algorithms_exe\\result\\standard_gsa_res.json"

        self.parameters = [AlgorithmParameter.get_MI(), AlgorithmParameter.get_NP(), AlgorithmParameter.get_KN(),
                           AlgorithmParameter.get_IG(), AlgorithmParameter.get_G0(), AlgorithmParameter.get_AG(),
                           AlgorithmParameter.get_EC(), AlgorithmParameter.get_RN(), AlgorithmParameter.get_RP(),
                           AlgorithmParameter.get_gamma()]

    def get_identifier_name(self) -> str:
        name = ("s_gsa_" +
                self.parameters[0].get_abbreviation() + "=" + str(self.parameters[0].get_selected_values()) + "_" +
                self.parameters[1].get_abbreviation() + "=" + str(self.parameters[1].get_selected_values()) + "_" +
                self.parameters[2].get_abbreviation() + "=" + str(self.parameters[2].get_selected_values()) + "_" +
                self.parameters[3].get_abbreviation() + "=" + str(self.parameters[3].get_selected_values()) + "_" +
                self.parameters[4].get_abbreviation() + "=" + str(self.parameters[4].get_selected_values()) + "_" +
                self.parameters[5].get_abbreviation() + "=" + str(self.parameters[5].get_selected_values()) + "_" +
                self.parameters[6].get_abbreviation() + "=" + str(self.parameters[6].get_selected_values()) + "_" +
                self.parameters[8].get_abbreviation() + "=" + str(self.parameters[8].get_selected_values()) + "_" +
                self.parameters[9].get_abbreviation() + "=" + str(self.parameters[9].get_selected_values()))
        return name
