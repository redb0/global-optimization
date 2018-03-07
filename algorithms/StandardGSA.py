from algorithms.GSA import GSA
import alg_parameters


class StandardGSA(GSA):
    def __init__(self):
        super().__init__()
        self.name = "Standard GSA"
        self.full_name = "Гравитационный поиск"
        self.parameters = [alg_parameters.get_MI(), alg_parameters.get_NP(), alg_parameters.get_KN(),
                           alg_parameters.get_IG(), alg_parameters.get_G0(), alg_parameters.get_AG(),
                           alg_parameters.get_EC(), alg_parameters.get_RN(), alg_parameters.get_RP()]

    # def get_param_obj(self, key):
    #     for p in self.parameters:
    #         if key == p.abbreviation:
    #             return p

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


if __name__ == '__main__':
    main()
