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

    def get_abbreviation_params(self) -> List[str]:
        """Метод получения списка аббревиатур параметров алгоритма"""
        abr = [i.get_abbreviation() for i in self.parameters]
        return abr

    def get_description_param(self, abr: str) -> str:
        """Метод возвращает полное название параметра по его аббревиатуре"""
        for p in self.parameters:
            if abr == p.abbreviation:
                return p.name

    def get_value_param_on_abbreviation(self, abr: str):
        """Метод возвращает значение параметра алгоритма по его аббревиатуре"""
        for p in self.parameters:
            if abr == p.abbreviation:
                return p.get_selected_values()

    # def get_name_params(self) -> List[str]:
    #     return list(self.parameters.values())

    # def get_keys_params(self) -> List[str]:
    #     return list(self.parameters.keys())
