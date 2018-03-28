import json
import random
from functools import wraps
import warnings

from PyQt5.QtWidgets import QComboBox
from typing import List, Union

from AlgorithmParameter import AlgorithmParameter
from algorithms.Algorithm import Algorithm


def get_max_step(sb, w):
    """
    Функция-замыкание. Возвращает функцию устанавливающую максимальное значение виджета QSpinBox или QDoubleSpinBox. 
    Максимальное значение зависит от значения виджета, переданного в эту функцию.
    :param sb: виджет от которого зависит максимальное значение 
    :param w: виджет которому будет устанавливаться максимальное значение
    :return: Возвращает функцию устанавливающую максимальное значение виджета QSpinBox или QDoubleSpinBox. 
             Возвращаемая функция принимает второе значение от которого будет зависеть максимальное значение, 
             установленное в переданный виджет
    """
    def f(x1):
        delta = abs(sb.value() - x1)
        # print(delta)
        w.setMaximum(delta)
        # return abs(x2 - x1)

    return f


def deprecated(message=None):
    """
    Декоратор для устаревших функции.
    
    Этот декоратор можно использовать для обозначения устаревших функций. 
    Это приведет к выводу переданного либо стандартного сообщения при использовании функции
    :param message: сообщение которое выведется при использовании функции, 
                    если None - выведется встроенное сообщение
    :return: возвращает функцию-замыкание, принимающую декорируемую функцию.
    """
    def decorator(func):
        @wraps(func)  # копируем имя и docstring декорируемой функции
        def wrapper(*args, **kwargs):
            """
            Оберточная функция.
            :return: 
            """
            # side-effect (побочный эффект) в виде выключения фильтра
            warnings.simplefilter("always", DeprecationWarning)
            if message is not None:
                # warnings.warn(message, category=DeprecationWarning, stacklevel=2)
                warnings.warn("Call to deprecated function {0}. \n Explanation: {1}".format(func.__name__, message),
                              category=DeprecationWarning, stacklevel=2)  # Explanation - объяснение
            else:
                warnings.warn("Call to deprecated function (Вызов устаревшей функции) {}.".format(func.__name__),
                              category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def write_json(file_name: str, data: Union[list, dict]) -> None:
    """
    Функция записи данных в json файл.
    :param file_name: имя файла в виде строки, куда будет производиться запись 
    :param data: данные для записи в виде словаря со строковыми ключами
    :return: None
    """
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def read_json(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def add_in_json(file: str, data: dict) -> None:
    """
    Функция добавления данных в json-файл.
    Добавление происходит путем считывания данных в словарь, 
    добавления данных к словарю и запись его в файл.
    :param file: путь до файла, str.
    :param data: данные для дозаписи в виде словаря (dict).
    :return: -
    """
    with open(file, 'r', encoding='utf-8') as f:
        # Установить указатель в начало файла
        f.seek(0, 0)
        data_from_file = json.load(f)
    data_from_file.update(data)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data_from_file, f)


def create_json_file(file: str):
    """Функция создания пустого json-файла"""
    with open(file, 'w', encoding='utf-8') as f:
        pass
        # Установить указатель в начало файла
        # f.seek(0, 0)


def overwrite_field_json(file_path: str, field_name: str, value) -> str:
    """
    Функция перезаписи значения поле в json-файле.
    Перезапись происходит путем считывания всего файла, 
    поиска нужного поля и исправления его значения, и записи новых данных.
    :param file_path  : путь до файла, который необходимо изменить.
    :param field_name : имя поля, значение которого необходимо поменять.
    :param value      : новое значение поля.
    :return: пустая строка, если ошибок нет, в противном случае строка с текстом ошибки.
    """
    error = ""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if field_name in list(data.keys()):
        data[field_name] = value
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return error
    else:
        error = "Поле с именем " + field_name + " в файле: " + file_path + " не существует."
        return error


def lies_in_interval(x, left, right) -> bool:
    """
    Функция проверки значения x на принадлежность отрезку [left, right].
    :param x: значение
    :param left: левая граница отрезка
    :param right: правая граница отрезка
    :return: True - если точка лежит в интервале, иначе - False.
    """
    if (x >= left) and (x <= right):
        return True
    return False


def lies_in_epsilon(x, c, e) -> bool:
    """
    Функция проверки значения x на принадлежность отрезку выда [c - e, c + e].
    :param x: значение
    :param c: значение попадание в epsilon-окрестность которо необходимо проверить
    :param e: epsilon-окрестность вокруг значения c
    :return: True - если точка лежит в интервале, иначе - False.
    """
    if (x >= (c - e)) and (x <= (c + e)):
        return True
    return False


def to_dict(parameters: List[AlgorithmParameter], **kwargs) -> dict:
    """
    Преобразование списка с параметрами в словарь для передачи в алгоритм.
    К словарю можно присоеденить переданные именные аргументы.
    Возвращается словать вида: {"Сокращенное название": значение параметра}
    :param parameters: список параметров, который нужно преобразовать
    :param kwargs: именные аргументы для включения в словарь
    :return: словарь с параметрами для передачи в алгоритм и записи в json.
    """
    d = {}
    for p in parameters:
        d.update({p.abbreviation: p.selected_values})
    for name in kwargs.keys():
        d.update({name: kwargs.get(name)})
    return d


def generate_rand_int_list(len_list=10):
    numbers = list(range(len_list))
    for i in range(len_list):
        x = random.randrange(0, len_list)
        numbers[i], numbers[x] = numbers[x], numbers[i]
    return numbers


def fill_combobox_list(cmb: QComboBox, data: list) -> None:
    """
    Функция заполнения нескольких комбобоксов данными, содержащимися в list.
    :param cmb: QComboBox, которые нужно заполнить
    :param data: 
    :return: 
    """
    cmb.clear()
    for k in data:
        cmb.addItem(str(k))


def fill_combobox_list_alg(data: List[Algorithm], *args: QComboBox) -> None:
    """
    Функция заполнения нескольких комбобоксов названиями алгоритмов и экземплярами их классов.
    :param data: список содержащий экземпляры наследников Algorithm.
    :param args: QComboBox, которые нужно заполнить
    :return: 
    """
    for cmb in args:
        cmb.clear()
        for k in data:
            cmb.addItem(k.get_full_name(), k)


def clear_combobox(*args: QComboBox) -> None:
    for cmb in args:
        cmb.clear()

