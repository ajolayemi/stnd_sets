#!/usr/bin/env python

from PyQt5.QtWidgets import (QApplication, QLabel,
                             QWidget, QFormLayout,
                             QFileDialog, QVBoxLayout,
                             QMainWindow, QPushButton,
                             QMessageBox, QComboBox,
                             QProgressBar, QLineEdit)
from PyQt5.QtGui import QFont

# Self defined modules
from modules import settings
from helper_modules import helper_functions


class UiWindow(QMainWindow):
    """ User interface window """

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle(settings.WIN_TITLE)
        self.resize(300, 200)
        self.centralWidget = QWidget()

        self.windowLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.windowLayout)
        self.setCentralWidget(self.centralWidget)

    def _addWidgets(self):
        username = helper_functions.get_user_name()
        self.greetingsLabel = QLabel(f'<h1>Ciao {username}')
        self.windowLayout.addWidget(self.greetingsLabel)

        self.buttonsLabel = '<b>---></b>'

        self.fonts = QFont('Times', 13)

        self.choiceCombo = QComboBox()
        self.choiceCombo.addItems(['Manualistica', 'Ispezione BIO'])
        self.choiceCombo.setFont(self.fonts)
        self.choiceCombo.setCurrentIndex(0)

        self.choiceComboLabel = QLabel('Per ')
        self.choiceComboLabel.setFont(QFont('Italics', 13))

        self.uploadSetsButton = QPushButton('Caricare STND_SETS')
        self.uploadSetsButton.setFont(self.fonts)
        self.uploadSetsButton.setStyleSheet('color: blue')

        self.uploadManualButton = QPushButton('Caricare Manuale')
        self.uploadManualButton.setFont(self.fonts)

        self.generateManualButton = QPushButton('Generare Manuale')
        self.generateManualButton.setFont(self.fonts)

        self.closeButton = QPushButton('Chiudi')
        self.closeButton.setFont(self.fonts)
        self.closeButton.setStyleSheet('color: red')

        buttonsList = [self.uploadSetsButton, self.uploadManualButton,
                       self.generateManualButton, self.closeButton]

        # Form Layout
        self.formLayout = QFormLayout()

        self.formLayout.addRow(self.choiceComboLabel, self.choiceCombo)

        for button in buttonsList:
            self.formLayout.addRow(self.buttonsLabel, button)

        self.progressBar = QProgressBar()
        self.formLayout.addRow(self.progressBar)

        self.windowLayout.addLayout(self.formLayout)


if __name__ == '__main__':
    pass
