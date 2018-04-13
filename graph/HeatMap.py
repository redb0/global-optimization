import numpy as np

from Settings import Settings
from graph.Graph import Graph


class HeatMap(Graph):
    def __init__(self, title, alg, param, axis_range):
        super().__init__(width=5, height=6, dpi=100, fontsize=12)
        self._title = title
        self._algorithms = alg
        self._param = param
        self.axis_range = axis_range
        self._settings = Settings()

    def plot(self):
        x, y, data = self.make_data()

    def make_data(self):
        x = np.arange(self.min_range, self.max_range, self.step)
        x_name = self._param.get_abbreviation()
        y = np.arange(self.min_range, self.max_range, self.step)
        print(x)

        probability = []
        for i in range(len(self.axis_range)):
            p = []
            for j in range(len(self.axis_range[i])):
                stock_value = self._algorithms.get_value_param_on_abbreviation(x_name)


        for alg in self._algorithms:
            y1 = []
            stock_value = alg.get_value_param_on_abbreviation(x_name)
            for i in range(len(x)):
                alg.set_parameter(x_name, x[i])
                if os.path.isfile(self._settings.abs_path_test_func):
                    probability = alg.find_probability_estimate(self._settings.real_extrema,
                                                                self._settings.epsilon,
                                                                self._settings.abs_path_test_func,
                                                                number_runs=self._settings.number_of_runs)
                else:
                    return np.array([]), [], "Не выбрана тестовая функция."
                print(probability)
                y1.append(probability)
            alg.set_parameter(x_name, stock_value)
            y.append(y1)
        print(y)
        return x, y, ""
