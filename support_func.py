import json
import random
from functools import wraps
import warnings

import numpy as np
from PyQt5.QtWidgets import QComboBox, QFileDialog
from typing import List, Union

from AlgorithmParameter import AlgorithmParameter


Num = Union[int, float]


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
        w.setMaximum(delta)

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


def create_json_file(file: str) -> None:
    """Функция создания пустого json-файла"""
    with open(file, 'w', encoding='utf-8') as _:
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


def lies_in_interval(x: Num, left: Num, right: Num) -> bool:
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


def lies_in_epsilon(x: Num, c: Num, e: Num) -> bool:
    """
    Функция проверки значения x на принадлежность отрезку выда [c - e, c + e].
    :param x: значение
    :param c: значение попадание в epsilon-окрестность которого необходимо проверить
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


def generate_rand_int_list(len_list=10) -> List[int]:
    """
    Функция генерации списка целых чисел. 
    Конечный список содержит числа от 0 до len_list в случайном порядке.
    :param len_list: длина генерируемого списка
    :return: список длиной len_list с целыми числами в случайном порядке.
    """
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


def fill_combobox_list_alg(data, *args: QComboBox) -> None:
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
    """Очистака комбобоксов"""
    for cmb in args:
        cmb.clear()


def open_file_dialog(title: str, file_filter: str, parent) -> str:
    """
    Метод открытия диалогового окна для выбора файла.
    :return: путь файла в виде строки, если он выбран, иначе пустая строка.
    """
    options = QFileDialog.Options()
    # options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getOpenFileName(parent, title, "",
                                               file_filter, options=options)
    if file_name:
        return file_name
    return ""


def combinations(ar):
    """
    Генератор комбинаций.
    >>> x = [1, 2, 3]
    >>> y = [4, 5, 6, 7]
    >>> list(combinations([x, y]))
    [[1, 4], [1, 5], [1, 6], [1, 7], [2, 4], [2, 5], [2, 6], [2, 7], [3, 4], [3, 5], [3, 6], [3, 7]]
    >>> list(combinations([]))
    [[]]
    >>> list(combinations([[]]))
    [[]]
    >>> list(combinations([[1, 2, 3]]))
    [[1], [2], [3]]
    
    :param ar: список со списками
    :return: генератор, возвращающий комбинации элементов списков
    """
    idxs = [0 for _ in range(len(ar))]
    f = True
    if len(ar) == 0:
        yield []
        f = False
    while f:
        combin = []
        for i in range(len(ar)):
            if len(ar[i]) == 0:
                f = False
                continue
            combin.append(ar[i][idxs[i]])
            if i == len(ar) - 1:
                j = len(idxs) - 1
                while j >= 0:
                    idxs[j] += 1
                    if idxs[j] == len(ar[j]):
                        if j == 0:
                            f = False
                        idxs[j] = 0
                        j -= 1
                    else:
                        break
        yield combin
    raise StopIteration


def get_delta(min_z, max_z, delta=0.5, l=0.5):
    j = 1
    while min_z < max_z:
        min_z = min_z + (delta * j)
        yield min_z
        j = j + l


def json_to_slice(data, field: str):
    res = []
    for d in data:
        res.append(d[field])
    return res


def make_report(data, file_name: str) -> None:
    d = {"min_time": 0,
         "max_time": 0,
         "mean_time": 0,
         "min_iter": 0,
         "max_iter": 0,
         "mean_iter": 0}

    run_time = json_to_slice(data, 'run_time')
    stop_iter = json_to_slice(data, 'stop_iteration')
    d['min_time'] = min(run_time)
    d['max_time'] = max(run_time)
    d['mean_time'] = np.mean(run_time)
    d['min_iter'] = min(stop_iter)
    d['max_iter'] = max(stop_iter)
    d['mean_iter'] = np.mean(stop_iter)

    write_json(file_name, d)
