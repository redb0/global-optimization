import AlgorithmParameter
from Settings import Settings
from algorithms.StandardSAC import StandardSAC


class AcsaSAC(StandardSAC):
    """
    Алгоритм селективного усреднения координат 
    с нессиметричным изменением области поиска.
    SAC with asymmetric change of search area.
    """
    def __init__(self):
        super().__init__()
        self.name = "SAC-ACSA"
        self.full_name = "Метод селективного усреднения с ассиметричной областью"
        self._relative_path = "..\\algorithms_exe\\sac_acsa.exe"
        self.config_file = "..\\algorithms_exe\\sac_acsa_config.json"
        self.result_file_name = "..\\algorithms_exe\\result\\sac_acsa_res.json"
        self._process = None
        self._start_time = None

        self.parameters = [AlgorithmParameter.get_MI(), AlgorithmParameter.get_NP(), AlgorithmParameter.get_KN(),
                           AlgorithmParameter.get_gamma(), AlgorithmParameter.get_SF(), AlgorithmParameter.get_KQ(),
                           AlgorithmParameter.get_NF()]

        self.settings = Settings()
