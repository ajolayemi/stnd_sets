#!/usr/bin/env python

from PyQt5.QtWidgets import (QApplication, QLabel,
                             QWidget, QFormLayout,
                             QFileDialog, QVBoxLayout,
                             QMainWindow, QPushButton,
                             QMessageBox, QComboBox,
                             QProgressBar, QLineEdit,)
from PyQt5.QtGui import QFont, QIntValidator

# Self defined modules
import settings
from helper_modules import helper_functions, logger

MSG_BOX_FONTS = QFont('Italics', 13)


class UiWindow(QMainWindow):
    """ User interface window """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(settings.WIN_TITLE)
        self.resize(300, 200)
        self.centralWidget = QWidget()

        self.windowLayout = QVBoxLayout()
        self._addWidgets()
        self.centralWidget.setLayout(self.windowLayout)
        self.setCentralWidget(self.centralWidget)

        self._setInitialState()

        self._connectSlotsSignals()

        self.file_path = None

        self.logger_cls = logger.Logger(file_name=settings.LOG_FILE_NAME)

    def _connectSlotsSignals(self):
        self.closeButton.clicked.connect(self._closeButton)
        self.rowNumber.textChanged.connect(self._updateInitialState)
        self.uploadManualButton.clicked.connect(self._uploadManual)

    def _updateInitialState(self):
        """ Updates the app state when user has entered a value in the
        rowNumber widget. """
        if self.rowNumber.text() and self.file_path:
            self.uploadSetsButton.setEnabled(True)
            self.generateManualButton.setEnabled(True)
        elif self.rowNumber.text() and not self.file_path:
            self.uploadSetsButton.setEnabled(True)
        else:
            self.uploadSetsButton.setEnabled(False)
            self.generateManualButton.setEnabled(False)

    def _setInitialState(self):
        """ Set's initial state of the app by not allowing
        user to click on some buttons until value is entered
        for the number of rows. """
        self.uploadSetsButton.setEnabled(False)
        self.generateManualButton.setEnabled(False)

    def _uploadManual(self):
        """ Reacts to user click on the 'Caricare Manuale button' """
        self.progressBar.setValue(0)
        self.file_path = helper_functions.FileSelector().file_selector()
        if self.file_path:
            msg_to_log = f'User ({helper_functions.get_user_name()}) - selected ' \
                         f'"{self.file_path}" \nas input file for manual upload.'
            self.logger_cls.log_info_msg(msg_to_log)
            self._updateInitialState()
            helper_functions.output_communicator(
                msg_box_font=MSG_BOX_FONTS,
                button_pressed=self.uploadManualButton.text(),
                output_type=True,
                window_title=settings.WIN_TITLE
            )

        else:
            helper_functions.no_file_selected_error(
                msg_box_font=MSG_BOX_FONTS,
                window_title=settings.WIN_TITLE,
                button_pressed=self.uploadManualButton.text()
            )

    def _closeButton(self):
        ask_user = helper_functions.ask_before_close(
            msg_box_font=MSG_BOX_FONTS,
            window_tile=settings.WIN_TITLE
        )
        if ask_user == QMessageBox.Yes:
            self.close()

    def getComboItem(self):
        return self.choiceCombo.currentText()

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

        self.rowNumberLabel = QLabel('N°: ')
        self.rowNumberLabel.setFont(QFont('Italics', 13))

        self.rowNumber = QLineEdit()
        self.rowNumber.setPlaceholderText('Inserire n° righe...')
        self.rowNumber.setValidator(QIntValidator())
        self.rowNumber.setFont(QFont('Italics', 13))

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
        self.formLayout.addRow(self.rowNumberLabel, self.rowNumber)
        for button in buttonsList:
            self.formLayout.addRow(self.buttonsLabel, button)

        self.progressBar = QProgressBar()
        self.formLayout.addRow(self.progressBar)

        self.windowLayout.addLayout(self.formLayout)


if __name__ == '__main__':
    pass
