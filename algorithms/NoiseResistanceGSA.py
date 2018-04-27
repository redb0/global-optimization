import AlgorithmParameter
from algorithms.GSA import GSA


class NoiseResistanceGSA(GSA):
    """Алгоритм гравитационного поиска 
    модифицированный для лучшей работы 
    в условиях воздействия помех.
    Noise Resistance Gravitation Search Algorithm (NR-GSA)."""
    def __init__(self):
        super().__init__()
        self.name = "Noise Resistance GSA"
        self.full_name = "Помехоустойчивый алгоритм гравитационного поиска"

        self._relative_path = "..\\algorithms_exe\\nr_gsa.exe"  # пусть до exe-шника с алгоритмом на golang
        self.config_file = "..\\algorithms_exe\\nr_gsa_config.json"
        self.result_file = "..\\algorithms_exe\\result\\nr_gsa_res.json"

        self.parameters = [AlgorithmParameter.get_MI(), AlgorithmParameter.get_NP(), AlgorithmParameter.get_KN(),
                           AlgorithmParameter.get_IG(), AlgorithmParameter.get_G0(), AlgorithmParameter.get_AG(),
                           AlgorithmParameter.get_EC(), AlgorithmParameter.get_RN(), AlgorithmParameter.get_RP(),
                           AlgorithmParameter.get_gamma(), AlgorithmParameter.get_SF(), AlgorithmParameter.get_NF(),
                           AlgorithmParameter.get_KQ(), AlgorithmParameter.get_EndNP(), AlgorithmParameter.get_ILCNP()]

    def get_identifier_name(self) -> str:
        name = ("nr_gsa_" +
                self.parameters[0].get_abbreviation() + "=" + str(self.parameters[0].get_selected_values()) + "_" +
                self.parameters[1].get_abbreviation() + "=" + str(self.parameters[1].get_selected_values()) + "_" +
                self.parameters[2].get_abbreviation() + "=" + str(self.parameters[2].get_selected_values()) + "_" +
                self.parameters[3].get_abbreviation() + "=" + str(self.parameters[3].get_selected_values()) + "_" +
                self.parameters[4].get_abbreviation() + "=" + str(self.parameters[4].get_selected_values()) + "_" +
                self.parameters[5].get_abbreviation() + "=" + str(self.parameters[5].get_selected_values()) + "_" +
                self.parameters[10].get_abbreviation() + "=" + str(self.parameters[10].get_selected_values()) + "_" +
                self.parameters[11].get_abbreviation() + "=" + str(self.parameters[11].get_selected_values()) + "_" +
                self.parameters[12].get_abbreviation() + "=" + str(self.parameters[12].get_selected_values()) + "_" +
                self.parameters[13].get_abbreviation() + "=" + str(self.parameters[13].get_selected_values()) + "_" +
                self.parameters[14].get_abbreviation() + "=" + str(self.parameters[14].get_selected_values()))
        return name
