import alg_parameters
from algorithms.SAC import SAC


class StandardSAC(SAC):
    def __init__(self):
        super().__init__()
        self.name = "Standard SAC"
        self.full_name = "Метод селективного усреднения"

        self._relative_path = "algorithms_exe\\standard_sac.exe"  # пусть до exe-шника с алгоритмом на golang
        self.config_file = "algorithms_exe\\standard_sac_config.json"
        self.process = None

        self.parameters = [alg_parameters.get_MI(), alg_parameters.get_NP(), alg_parameters.get_KN()]

    def get_params_dict(self):
        d = {}
        for p in self.parameters:
            d.update({p.abbreviation: p.name})
        return d
