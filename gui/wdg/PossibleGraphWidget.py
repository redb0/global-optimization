from PyQt5 import QtCore

from PyQt5.QtWidgets import QWidget


class PossibleGraphWidget(QWidget):
    """Родительский класс для виджетов возможных графиков"""
    def get_widget(self):
        """Метод конструирования виджета"""
        pass

    def translate(self, s, s_1: str):
        return QtCore.QCoreApplication.translate(s, s_1)

    def delete_graph(self, w):
        """Метод удаления виджетв"""
        return w.deleteLater
