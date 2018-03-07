import alg_parameters
from algorithms.SAC import SAC


class StandardSAC(SAC):
    def __init__(self):
        super().__init__()
        self.name = "Standard SAC"
        self.full_name = "Метод селективного усреднения"
        self.parameters = [alg_parameters.get_MI(), alg_parameters.get_NP(), alg_parameters.get_KN()]

    def get_params_dict(self):
        d = {}
        for p in self.parameters:
            d.update({p.abbreviation: p.name})
        return d
