from typing import Union, List


class Parameter:
    """
    Класс для описания отдельной настройки программы
    Атрибуты:
        _name             : полное название настройки, для отображения в графическом интерфейсе
        _parameter_type   : типа параметра
        _present_value    : текущее значение
        _default_value    : значение по умолчанию
        _allowable_values : допустимые значения, если есть
    """

    def __init__(self, name: str, parameter_type, default_value, allowable_values=None):
        self._name = name
        self._parameter_type = parameter_type
        self._present_value = default_value
        self._default_value = default_value
        self._allowable_values = allowable_values

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def parameter_type(self) -> Union[type, List[type]]:
        return self._parameter_type

    @parameter_type.setter
    def parameter_type(self, value: Union[type, List[type]]) -> None:
        self._parameter_type = value

    @property
    def default_value(self) -> Union[int, float, bool, str]:
        return self._default_value

    @default_value.setter
    def default_value(self, value: Union[int, float, bool, str]) -> None:
        self._default_value = value

    @property
    def allowable_values(self) -> Union[int, float, bool, List[Union[int, float, bool]]]:
        return self._allowable_values

    @allowable_values.setter
    def allowable_values(self, value: Union[int, float, bool, List[Union[int, float, bool]]]) -> None:
        self._allowable_values = value

    @property
    def present_value(self):
        return self._present_value

    @present_value.setter
    def present_value(self, value) -> None:
        self._present_value = value

    def set_default_value(self):
        self._present_value = self._default_value
