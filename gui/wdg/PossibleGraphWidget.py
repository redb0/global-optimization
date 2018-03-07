from PyQt5 import QtCore

from PyQt5.QtWidgets import QWidget


class PossibleGraphWidget(QWidget):

    def get_widget(self):
        pass

    def translate(self, s, s_1: str):
        return QtCore.QCoreApplication.translate(s, s_1)

    def delete_graph(self, w):
        return w.deleteLater