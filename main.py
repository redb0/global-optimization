import sys
from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())

# TODO: добавить график дисперсии (как быть когда массим дисперсии двумерный) - функция, подключение ???

# TODO: интегрировать модуль конструирования тестовых функций (tf-generator)

if __name__ == '__main__':
    main()
