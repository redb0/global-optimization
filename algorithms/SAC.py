from algorithms.Algorithm import Algorithm


class SAC(Algorithm):
    """
    Класс для объединение алгоритмов класса SAC (алгоритм селективного усреднения координат).
    Добавляет наследнику поле class_alg со значением "SAC" 
    """
    def __init__(self):
        super().__init__()
        self.class_alg = "SAC"
