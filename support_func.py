import json
import os
from functools import wraps
import warnings
from typing import List, Union

from Parameters import Parameters


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


def write_json(file_name: str, data: dict) -> None:
    """
    Функция записи данных в json файл.
    :param file_name: имя файла в виде строки, куда будет производиться запись 
    :param data: данные для записи в виде словаря со строковыми ключами
    :return: None
    """
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def add_in_json(file: str, data: dict) -> None:
    # TODO: добавить документацию
    # data_from_file = {}
    with open(file, 'r', encoding='utf-8') as f:
        # Установить указатель в начало файла
        f.seek(0, 0)
        data_from_file = json.load(f)
    # if os.path.isfile(file):
    #     with open(file, 'r', encoding='utf-8') as f:
    #         # Установить указатель в начало файла
    #         f.seek(0, 0)
    #         data_from_file = json.load(f)
    # elif not os.path.isfile(file):
    #     f = open(file, 'a+')
    #     f.close()
    #     # with open(file, 'a+', encoding='utf-8') as f:  # тут нихрена не создается файл
    #     #     pass

    data_from_file.update(data)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data_from_file, f)


def create_json_file(file: str):
    """Функция создания пустого json-файла"""
    with open(file, 'w', encoding='utf-8') as f:
        pass
        # Установить указатель в начало файла
        # f.seek(0, 0)


def write_in_json(file_name: str, data: Union[list, dict]) -> None:
    """
    Запись данных в json файл
    :param file_name: путь до файла в виде строки
    :param data: данные, в виде списка либо словаря
    :return: 
    """
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f)


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


def to_dict(parameters: List[Parameters], **kwargs) -> dict:
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
