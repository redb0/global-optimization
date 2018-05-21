import os

from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtWidgets import QApplication


class UiAboutDialog(object):
    """Графический интерфейс окна "О программе" """
    def setup_ui(self, about_dialog):
        about_dialog.setObjectName("AboutDialog")
        about_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        about_dialog.resize(683, 443)
        about_dialog.setMinimumSize(QtCore.QSize(300, 0))
        about_dialog.setModal(True)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(about_dialog)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # фрейм для названия, копирайтинга и версии
        self.frame = QtWidgets.QFrame(about_dialog)
        self.frame.setStyleSheet("#frame { background: white; }")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.gridLayout = QtWidgets.QGridLayout(self.frame)  # QGridLayout - размещение объектов в сетке
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.logo = QtWidgets.QLabel(self.frame)
        self.logo.setText("Метсто для вашей рекламы")
        # self.bg.setPixmap(QtGui.QPixmap("../res/logo.png"))
        self.logo.setObjectName("bg")
        self.gridLayout.addWidget(self.logo, 0, 0, 5, 1)
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Times")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)  # 0 - строка, 1 - столбец, 1 - строка для растягивания, 1 - столбец для растягивания
        spacer_item = QtWidgets.QSpacerItem(363, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacer_item, 0, 2, 3, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        self.version_string = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.version_string.setFont(font)
        self.version_string.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.version_string.setObjectName("version_string")
        self.gridLayout.addWidget(self.version_string, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.frame)

        # фрейм для табвиджета
        self.frame_2 = QtWidgets.QFrame(about_dialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.frame_2)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_4.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_4.addWidget(self.textBrowser)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeWidget = QtWidgets.QTreeWidget(self.tab_2)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setDefaultSectionSize(185)
        self.treeWidget.header().setMinimumSectionSize(60)
        self.verticalLayout_3.addWidget(self.treeWidget)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.verticalLayout_2.setStretch(0, 10)
        self.verticalLayout_2.setStretch(1, 90)

        self.retranslate_ui(about_dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(about_dialog)

    def retranslate_ui(self, about_dialog):
        _translate = QtCore.QCoreApplication.translate
        about_dialog.setWindowTitle(_translate("AboutDialog", "GlOpPy - О программе"))
        self.label.setText(_translate("AboutDialog", "GlOpPy 2018"))
        self.label_3.setText(_translate("AboutDialog", "Copyright © 2018 Vladimir Voronov"))
        self.version_string.setText(_translate("AboutDialog", "Версия v0.1"))

        script_path = os.path.dirname(os.path.abspath(__file__))
        path_to_license = os.path.join(script_path, "../resource/license.html")
        with open(path_to_license, 'r') as f:
            license_html = f.read()

        self.textBrowser.setHtml(_translate("AboutDialog", license_html))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("AboutDialog", "License"))
        self.treeWidget.headerItem().setText(0, _translate("AboutDialog", "Name"))
        self.treeWidget.headerItem().setText(1, _translate("AboutDialog", "Author"))
        self.treeWidget.headerItem().setText(2, _translate("AboutDialog", "License"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("AboutDialog", "Qt 5"))
        self.treeWidget.topLevelItem(0).setText(1, _translate("AboutDialog", "The Qt Company"))
        self.treeWidget.topLevelItem(0).setText(2, _translate("AboutDialog", "GNU GPL 2.0/3.0/LGPL 3.0"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("AboutDialog", "Python 3"))
        self.treeWidget.topLevelItem(1).setText(1, _translate("AboutDialog", "Python Software Foundation"))
        self.treeWidget.topLevelItem(1).setText(2, _translate("AboutDialog", "Python Software Foundation License"))
        self.treeWidget.topLevelItem(2).setText(0, _translate("AboutDialog", "pyqt5"))
        self.treeWidget.topLevelItem(2).setText(1, _translate("AboutDialog", "Riverbank Computing Limited"))
        self.treeWidget.topLevelItem(2).setText(2, _translate("AboutDialog", "GNU GPL v3"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("AboutDialog", "3rd Party Software"))

    def to_utf(self, text):
        return QApplication.translate("AboutDialog", text, None)

