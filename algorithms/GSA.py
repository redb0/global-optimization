from algorithms.Algorithm import Algorithm


class GSA(Algorithm):
    """
    Класс для объединение алгоритмов класса Gravitation Search Algorithms (GSA).
    Добавляет наследнику поле class_alg со значением "GSA"
    """
    def __init__(self):
        super().__init__()
        self.class_alg = "GSA"
