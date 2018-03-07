from abc import ABCMeta, abstractmethod


class Graph:
    __metaclass__ = ABCMeta

    # TODO: возможно сделать абстрактным
    @abstractmethod
    def __init__(self):
        # self.name = name_param
        # self.algorithms = alg
        pass

    @abstractmethod
    def get_widget(self):
        pass
