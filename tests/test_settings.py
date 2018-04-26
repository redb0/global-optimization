import pytest

from Settings import Settings


class TestSettings:
    def setup(self):
        self.settings = Settings()

    def teardown(self):
        pass

    def test_min_flag(self):
        assert self.settings.min_flag == 1

        self.settings.min_flag = 1.2
        assert self.settings.min_flag == 1
        self.settings.min_flag = "qwe"
        assert self.settings.min_flag == 1
        self.settings.min_flag = 0
        assert self.settings.min_flag == 0

    def test_number_of_runs(self):
        assert self.settings.number_of_runs == 100

        self.settings.number_of_runs = -100
        assert self.settings.number_of_runs == 100
        self.settings.number_of_runs = 0
        assert self.settings.number_of_runs == 100
        self.settings.number_of_runs = 10
        assert self.settings.number_of_runs == 10

    def test_epsilon(self):
        assert self.settings.epsilon == 0.5

        self.settings.epsilon = 1
        assert self.settings.epsilon == 1
        self.settings.epsilon = 0.25
        assert self.settings.epsilon == 0.25
        self.settings.epsilon = [0.5, 0.25]
        assert self.settings.epsilon == [0.5, 0.25]
        self.settings.epsilon = [2, 0.25]
        assert self.settings.epsilon == [2, 0.25]

        self.settings.epsilon = "qwe"
        assert self.settings.epsilon == 0.5
        self.settings.epsilon = [0.5, "qwe"]
        print(self.settings.epsilon)
        assert self.settings.epsilon == 0.5

    def test_path(self):
        assert self.settings.abs_path_test_func == ""

        self.settings.abs_path_test_func = ""
        assert self.settings.abs_path_test_func == ""

        self.settings.abs_path_test_func = "C:\\Projects_Python\\GlobalOptimization2\\examples_tf\\func5.json"
        assert self.settings.abs_path_test_func == "C:\\Projects_Python\\GlobalOptimization2\\examples_tf\\func5.json"

        self.settings.abs_path_test_func = "C:\\Projects_Python\\GlobalOptimization2\\examples_tf\\f3_contour.png"
        assert self.settings.abs_path_test_func == ""
