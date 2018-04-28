import sys
from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())

# FIXME:

# TODO: Добавить в окно настроек отображение координат глобального минимума, либо None если не указан - DONE
# TODO: Добавить в окно настроек отображение координат глобального максимума, либо None если не указан - DONE
# TODO: добавить график движения лучшей точки к экстремуму со стрелками на фоне графика изолиний
# TODO: интегрировать модуль конструирования тестовых функций (tf-generator)

if __name__ == '__main__':
    main()
