import sys
from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
