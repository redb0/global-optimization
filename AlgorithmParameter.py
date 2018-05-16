class AlgorithmParameter:
    def __init__(self, abbreviation: str, name: str, p_type: type, tex: str,
                 allowable_values=None, default_value=None):
        # TODO: возможно добавить проверку возможных значений на тип
        self.name = name
        self.abbreviation = abbreviation
        self.p_type = p_type
        self.allowable_values = allowable_values
        self.selected_values = default_value
        self.default_value = default_value
        self._label_TeX = tex

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
        self.selected_values = self.p_type(values)

    @property
    def label_TeX(self):
        return self._label_TeX


def get_MI():
    p = AlgorithmParameter("MI", "Количество итераций", int, "$T$", default_value=500)
    return p


def get_NP():
    p = AlgorithmParameter("NP", "Количество точек", int, "$N$", default_value=200)
    return p


def get_KN():
    p = AlgorithmParameter("KN", "Коэффициент помехи", float, "$SNR(k{_{SN}})$", default_value=0.0)
    return p


def get_IG():
    p = AlgorithmParameter("IG", "Индекс функции изменения гравитационной постоянной", int, "$i{_g}$",
                           [1, 2, 3, 4], default_value=1)
    # TODO: добавить варианты тестовых функций
    return p


def get_G0():
    p = AlgorithmParameter("G0", "Начальное значение гравитационной постоянной", float, "$G{_0}$", default_value=100)
    return p


def get_AG():
    p = AlgorithmParameter("AG", "Коэффициент альфа", float, "$\\alpha$", default_value=20)
    return p


def get_EC():
    # bool, [True, False]
    p = AlgorithmParameter("EC", "Использование элитных зондов", int, "$EC$", [1, 0], default_value=True)
    return p


def get_RN():
    p = AlgorithmParameter("RN", "Норма линейного пространства", int, "$Rn$", [1, 2], default_value=2)
    return p


def get_RP():
    p = AlgorithmParameter("RP", "Степень влияния расстояния", int, "$Rp$", default_value=1)
    return p


def get_gamma():
    p = AlgorithmParameter("GA", "Коэффициент гамма", float, "$\\gamma$", default_value=1)
    return p


def get_SF():
    p = AlgorithmParameter("SF", "Коэффициент селективности", float, "$s$", default_value=100)
    return p


def get_KQ():
    p = AlgorithmParameter("KQ", "Коэффициент q", float, "$q$", default_value=1)
    return p


def get_NF():
    p = AlgorithmParameter("NF", "Индекс ядерной функции", int, "$nf$", default_value=1, allowable_values=[1, 2, 3, 4])
    return p


def get_EndNP():
    p = AlgorithmParameter("EndNP", "Конечное количество точек", int, "$N_{end}$", default_value=10)
    return p


def get_ILCNP():
    p = AlgorithmParameter("ILCNP", "Индекс закона изменения количества точек", int, "$i{_cnp}$",
                           default_value=1, allowable_values=[1, 2, 3, 4, 5, 6, 7])
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
    elif key == "GA":
        p = get_gamma()
    elif key == "SF":
        p = get_SF()
    elif key == "KQ":
        p = get_KQ()
    elif key == "NF":
        p = get_NF()
    elif key == "EndNP":
        p = get_EndNP()
    elif key == "ILCNP":
        p = get_ILCNP()

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
