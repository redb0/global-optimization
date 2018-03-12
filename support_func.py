import json
from functools import wraps
import warnings


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
    with open(file_name, 'wb') as f:
        json.dump(data, f)
