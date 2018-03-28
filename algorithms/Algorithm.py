from typing import List


class Algorithm:
    def __init__(self):
        self.class_alg = ""
        self.name = ""
        self.full_name = ""
        self.parameters = None

    def run(self, result_file_name: str, file_test_func: str):
        pass

    def get_class(self) -> str:
        return self.class_alg

    def get_name(self) -> str:
        return self.name

    def get_full_name(self):
        return self.full_name

    def get_parameters(self):
        return self.parameters

    def get_identifier_name(self) -> str:
        """Метод генерации уникального имени"""
        pass

    # def get_name_params(self) -> List[str]:
    #     return list(self.parameters.values())

    # def get_keys_params(self) -> List[str]:
    #     return list(self.parameters.keys())
