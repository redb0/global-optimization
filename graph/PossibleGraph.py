class PossibleGraph:
    def __init__(self, type_graph: str, parameters, params_range, algs):
        self.type_graph = type_graph
        # self.dimension = dimension
        self.parameters = parameters
        # self.types_params = types_params
        self.params = params_range
        self.algorithms = algs

    def plot(self):
        pass

    def get_type_graph(self) -> str:
        return self.type_graph

    # def get_types_param(self):
    #     return self.types_params

    def get_parameters_obj(self):
        return self.parameters

    def add_params(self, parameter, range_p):
        self.parameters.append(parameter)
        # self.types_params.append(type_p)
        self.params.append(range_p)

    def add_param_range(self, range_p):
        self.params.append(range_p)

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def get_param_range(self):
        return self.params
