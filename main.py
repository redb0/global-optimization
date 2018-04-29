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
# TODO: добавить точечный график количества пройденных итераций.
# TODO: добавить график сходимости по значению функции.
# TODO: добавить график сходимости по координатам.
# TODO: добавить график дисперсии (как быть когда массим дисперсии двумерный)???
# TODO: сохранение отчета (json) (максимальное, минимальное, среднее время выполнения алгоритма, количество итераций)
# TODO: интегрировать модуль конструирования тестовых функций (tf-generator)

if __name__ == '__main__':
    main()
