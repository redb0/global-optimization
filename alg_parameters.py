class Parameters:
    def __init__(self, abbreviation: str, name: str, p_type: type,
                 allowable_values=None, default_value=None):
        # TODO: возможно добавить проверку возможных значений на тип
        self.name = name
        self.abbreviation = abbreviation
        self.p_type = p_type
        self.allowable_values = allowable_values
        self.selected_values = default_value
        self.default_value = default_value

    # метод можно вызывать прямиком из класса, без создания экземпляра
    @staticmethod
    def get_list_key(list_obj):
        """
        Метод для создания списка из сокращенных обозначений параметров.
        Статический метод. 
        Пример вызова: Parameters.get_list_key(list_obj)
        :param list_obj: список экземпляров класса Parameters.
        :return: список сокращенных обозначений
        """
        list_key = []
        for obj in list_obj:
            list_key.append(obj.get_abbreviation())
        return list_key

    def get_abbreviation(self) -> str:
        return self.abbreviation

    def get_type(self) -> type:
        return self.p_type

    def get_name(self) -> str:
        return self.name

    def get_allowable_values(self):
        return self.allowable_values

    def get_selected_values(self):
        return self.selected_values

    def get_default_value(self):
        return self.default_value

    def set_selected_values(self, values) -> None:
        self.selected_values = values


def get_MI():
    p = Parameters("MI", "Количество итераций", int, default_value=500)
    return p


def get_NP():
    p = Parameters("NP", "Количество точек", int, default_value=200)
    return p


def get_KN():
    p = Parameters("KN", "Коэффициент помехи", float, default_value=0.0)
    return p


def get_IG():
    p = Parameters("IG", "Индекс функции изменения гравитационной постоянной", int, [1, 2, 3, 4], default_value=1)
    # TODO: добавить варианты тестовых функций
    return p


def get_G0():
    p = Parameters("G0", "Начальное значение гравитационной постоянной", float, default_value=100)
    return p


def get_AG():
    p = Parameters("AG", "Коэффициент альфа", float, default_value=20)
    return p


def get_EC():
    p = Parameters("EC", "Использование элитных зондов", bool, [True, False], default_value=True)
    return p


def get_RN():
    p = Parameters("RN", "Норма линейного пространства", int, [1, 2], default_value=2)
    return p


def get_RP():
    p = Parameters("RP", "Степень влияния расстояния", int, default_value=1)
    return p


def get_parameters(key: str):
    p = None
    if key == "RP":
        p = get_RP()
    elif key == "RN":
        p = get_RN()
    elif key == "EC":
        p = get_EC()
    elif key == "AG":
        p = get_AG()
    elif key == "G0":
        p = get_G0()
    elif key == "IG":
        p = get_IG()
    elif key == "KN":
        p = get_KN()
    elif key == "NP":
        p = get_NP()
    elif key == "MI":
        p = get_MI()

    # if key == "RN":
    #     p = get_RN()
    # if key == "RN":
    #     p = get_RN()
    # if key == "RN":
    #     p = get_RN()
    return p


def get_param_from_list(list_obj, key):
    for obj in list_obj:
        if key == obj.get_abbreviation():
            return obj
    return None


def get_param_on_name(list_obj, name):
    for obj in list_obj:
        if name == obj.get_name():
            return obj
    return None
