class PossibleGraph:
    def __init__(self, type_graph: str, parameters, params_range, algs):
        self.type_graph = type_graph
        # self.dimension = dimension
        self.parameter = parameters
        # self.types_params = types_params
        self.range = params_range
        self.algorithms = algs

    def plot(self):
        pass

    def get_type_graph(self) -> str:
        return self.type_graph

    def get_parameters_obj(self):
        return self.parameter

    def add_params(self, parameter, range_p):
        self.parameter.append(parameter)
        self.range.append(range_p)

    def add_param_range(self, range_p):
        self.range.append(range_p)

    def add_parameter(self, parameter):
        self.parameter.append(parameter)

    def get_param_range(self):
        return self.range
