from graph.Graph import Graph


class PointGraph(Graph):
    def __init__(self, name_param, alg, possible_values):
        super().__init__()
        self.name = name_param
        self.algorithms = alg
        self.possible_values = possible_values

    def get_widget(self):
        pass

