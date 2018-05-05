from typing import List, Union

import numpy as np


def get_test_function_method_min(n: int, a: List[List[float]], c: List[List[float]],
                                 p: List[List[float]], b: List[float]):
    """
    Функция-замыкание, генерирует и возвращает тестовую функцию, применяя метод Фельдбаума, 
    т. е. применяя оператор минимума к одноэкстремальным степенным функциям.
    :param n: количество экстремумов, целое число >= 1
    :param a: список коэффициентов крутости экстремумов (длиной n), чем выше значения, 
              тем быстрее функция убывает/возрастает и тем уже область экстремума, List[List[float]]
    :param c: список координат экстремумов длиной n, List[List[float]]
    :param p: список степеней гладкости в районе экстремума, 
              если 0<p[i][j]<=1 функция в точке экстремума будет угловой
    :param b: список значений функции (длиной n) в экстремуме, List[float], len(b) = n
    :return: возвращает функцию, которой необходимо передавать одномерный список координат точки, 
             возвращаемая функция вернет значение тестовой функции в данной точке
    """
    def func(x):
        l = []
        for i in range(n):
            res = 0
            for j in range(len(x)):
                res = res + a[i][j] * np.abs(x[j] - c[i][j]) ** p[i][j]
            res = res + b[i]
            l.append(res)
        res = np.array(l)
        return np.min(res)
    return func


def get_tf_hyperbolic_potential_abs(n: int, a: List[float], c: List[List[float]],
                                    p: List[List[float]], b: List[float]):
    """
    Функция-замыкание. Генерирует и возвращает тестовую функцию, 
    основанную на гиперболических потенциалах с аддитивными модульными функциями в знаменателе.
    :param n: количество экстремумов, целое число >= 1
    :param a: одномерный список коэффициентов (длиной n), определяющих крутость функции в районе экстремума
    :param c: двумерный список координат экстремумов длиной n, List[List[float]]
    :param p: 
    :param b: одномерный список коэффициентов (длиной n), определяющих значения функции в точках экстремумов
    :return: возвращает функцию, которой необходимо передавать одномерный список координат точки, 
             возвращаемая функция вернет значение тестовой функции в данной точке
    """
    def func(x):
        value = 0
        for i in range(n):
            res = 0
            for j in range(len(x)):
                res = res + np.abs(x[j] - c[i][j]) ** p[i][j]
            res = a[i] * res + b[i]
            res = -(1 / res)
            value = value + res
        return value
    return func


def get_tf_hyperbolic_potential_sqr(n: int, a: List[List[float]], c: List[List[float]], b):
    """
    Функция-замыкание. Генерирует и возвращает тестовую функцию, 
    основанную на гиперболических потенциалах с иддитивными квадратичными функциями в знаменателе.
    :param n: количество экстремумов, целое число >= 1
    :param a: 
    :param c: двумерный список координат экстремумов длиной n, 
              List[List[float]], размерность n * m, m - размерность задачи
    :param b: одномерный список коэффициентов (длиной n), определяющих значения функции в точках экстремумов
    :return: возвращает функцию, которой необходимо передавать одномерный список координат точки, 
             возвращаемая функция вернет значение тестовой функции в данной точке
    """
    def func(x):
        value = 0
        for i in range(n):
            res = 0
            for j in range(len(x)):
                res = res + a[i][j] * (x[j] - c[i][j]) ** 2  # правильно ли стоит a???????
            res = res + b[i]
            res = -(1 / res)
            value = value + res
        return value
    return func


def get_tf_exponential_potential(n: int, a: List[float], c: List[List[float]],
                                 p: List[List[float]], b: List[float]):
    """
    Функция-замыкание. Генерирует и возвращает тестовую функцию, 
    основанную на экспоненциальных потенциалах с аддитивными модульными функциями в знаменателе.
    :param n: количество экстремумов, целое число >= 1
    :param a: одномерный список коэффициентов (длиной n), определяющих крутость функции в районе экстремума
    :param c: двумерный список координат экстремумов, List[List[float]], размерность n * m, m - размерность задачи
    :param p: двумерный список степеней гладкости функции в районе экстремума, List[List[float]], размерность n * m
    :param b: одномерный список коэффициентов (длиной n), определяющих значения функции в точках экстремумов
    :return: возвращает функцию, которой необходимо передавать одномерный список координат точки, 
             возвращаемая функция вернет значение тестовой функции в данной точке
    """
    def func(x):
        value = 0
        for i in range(n):
            res = 0
            for j in range(len(x)):
                res = res + np.abs(x[j] - c[i][j]) ** p[i][j]
            res = (-b[i]) * np.exp((-a[i]) * res)
            value = value + res
        return value
    return func


def get_test_func(type_func: str, n: int,
                  a: List[Union[List[float], float]], c: List[List[float]], p: List[List[float]], b: List[float]):
    if type_func == "feldbaum_function":
        func = get_test_function_method_min(n, a, c, p, b)
    elif type_func == "hyperbolic_potential_abs":
        func = get_tf_hyperbolic_potential_abs(n, a, c, p, b)
    elif type_func == "exponential_potential":
        func = get_tf_exponential_potential(n, a, c, p, b)
    else:
        func = None
    return func
