from PyQt5.QtWidgets import QDialog

from gui.about_dialog_ui import UiAboutDialog


class AboutDialog(QDialog):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        self.ui = UiAboutDialog()
        self.ui.setup_ui(self)
