import unittest
from unittest.mock import patch

from algorithms.Algorithm import Algorithm


class TestAlgorithm(unittest.TestCase):
    def setUp(self):
        self.alg = Algorithm()
        self.alg._exe_relative_path = "..\\algorithms_exe\\1.exe"
        self.alg.config_file = "..\\algorithms_exe\\config.json"

    @patch("subprocess.Popen")
    @patch("time.time")
    def test_run(self, no_time, no_popen):
        result_file_name = "..\\algorithms_exe\\res.json"
        file_test_func = "\\examples_tf\\func3.json"

        no_popen.return_value = None
        no_time.return_value = None

        path = self.alg.run(result_file_name, file_test_func)

        args = list(no_popen.call_args_list[0])[0][0]

        assert args[0].find(self.alg._exe_relative_path) != -1
        assert args[1] == ""
        assert args[2].find(self.alg.config_file) != -1
        assert args[3].find(file_test_func) != -1
        assert args[-1] == path

    def test_run_negative(self):
        self.alg._process = 1

        path = self.alg.run("", "")

        assert path == ""


if __name__ == "__main__":
    unittest.main()




