#!/usr/bin/env python

from PyQt5.QtWidgets import (QApplication, QLabel,
                             QWidget, QFormLayout,
                             QFileDialog, QVBoxLayout,
                             QMainWindow, QPushButton,
                             QMessageBox, QComboBox,
                             QProgressBar, QLineEdit,)
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import QThread

# Self defined modules
import settings
from helper_modules import helper_functions, logger
from database_reader import DatabaseReader
from worker_threads import SetUploader

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

        self.manual_file_path = None
        self.set_file_path = None

    def _connectSlotsSignals(self):
        self.closeButton.clicked.connect(self._closeButton)
        self.rowNumber.textChanged.connect(self._updateInitialState)
        self.uploadManualButton.clicked.connect(self._uploadManual)
        self.uploadSetsButton.clicked.connect(self._uploadSets)
        self.generateManualButton.clicked.connect(self._genManual)

    def _manualGenThread(self, file_path, row_num):
        pass

    def _genManual(self):
        initial_log = f'({helper_functions.get_user_name()}) clicked on ' \
                     f'{self.generateManualButton.text()}'
        settings.LOGGER_CLS.log_info_msg(initial_log)
        check_table = DatabaseReader()
        check_table.create_reader_con()
        if not check_table.table_is_empty():
            self._manualGenThread(self.manual_file_path,
                                  self.rowNumber.text())
        else:
            msg = 'Mi risulta che il database prodotti è vuoto'
            helper_functions.no_file_selected_error(
                msg_box_font=MSG_BOX_FONTS,
                custom_msg=msg,
                window_title=settings.WIN_TITLE
            )

    def _setThreadManager(self, set_file_path, total_row):
        self._thread = QThread()
        self._uploader_cls = SetUploader(file_path=set_file_path, row_num=total_row)
        # Move this process to a separate thread
        self._uploader_cls.moveToThread(self._thread)

        # Connect thread start to the method that upload sets
        self._thread.started.connect(self._uploader_cls.setUploader)

        # Update states
        self._uploader_cls.progress.connect(self.progressBar.setValue)
        self._uploader_cls.progress.connect(self._updateStateWhileBusy)
        self._uploader_cls.finished.connect(self._communicateSetSuccess)
        self._uploader_cls.unfinished.connect(self._communicateSetFailure)
        self._uploader_cls.finished.connect(self._setInitialState)
        self._uploader_cls.finished.connect(self._setInitialState)

        # Clean up
        self._uploader_cls.finished.connect(self._thread.quit)
        self._uploader_cls.unfinished.connect(self._thread.quit)
        self._uploader_cls.finished.connect(self._uploader_cls.deleteLater)
        self._uploader_cls.unfinished.connect(self._uploader_cls.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        # Run the thread
        self._thread.start()

    def _uploadSets(self):
        """ Logic behind set upload. It populates the product database
        used in this project. """
        # Log user click
        msg_to_log = f'({helper_functions.get_user_name()}) clicked on ' \
                     f'{self.uploadSetsButton.text()}'
        settings.LOGGER_CLS.log_info_msg(msg_to_log)

        self.progressBar.setValue(0)
        db_reader_cls = DatabaseReader()
        db_reader_cls.create_reader_con()
        # Check to see that database is empty, if it isn't
        if not db_reader_cls.table_is_empty():
            ask_user = helper_functions.ask_for_overwrite(
                msg_box_font=MSG_BOX_FONTS,
                window_tile=settings.WIN_TITLE
            )
            if ask_user == QMessageBox.Yes:
                db_reader_cls.drop_table()
                self.set_file_path = helper_functions.FileSelector().file_selector()
        else:
            self.set_file_path = helper_functions.FileSelector().file_selector()
        if not self.set_file_path:
            helper_functions.no_file_selected_error(
                button_pressed=self.uploadSetsButton.text(),
                msg_box_font=MSG_BOX_FONTS,
                window_title=settings.WIN_TITLE
            )
        else:
            self._setThreadManager(set_file_path=self.set_file_path, total_row=self.rowNumber.text())

    def _updateStateWhileBusy(self):
        """ Updates the app's state when it is busy doing something else. """
        self.uploadSetsButton.setEnabled(False)
        self.uploadManualButton.setEnabled(False)
        self.generateManualButton.setEnabled(False)
        self.closeButton.setEnabled(False)

    def _communicateSetSuccess(self):
        helper_functions.output_communicator(
            msg_box_font=MSG_BOX_FONTS,
            output_type=True,
            button_pressed=self.uploadSetsButton.text(),
            window_title=settings.WIN_TITLE
        )

    def _communicateSetFailure(self):
        helper_functions.output_communicator(
            msg_box_font=MSG_BOX_FONTS,
            output_type=False,
            button_pressed=self.uploadSetsButton.text(),
            window_title=settings.WIN_TITLE
        )

    def _updateInitialState(self):
        """ Updates the app state when user has entered a value in the
        rowNumber widget. """
        if self.rowNumber.text() and self.manual_file_path:
            self.uploadSetsButton.setEnabled(True)
            self.generateManualButton.setEnabled(True)
        elif self.rowNumber.text() and not self.manual_file_path:
            self.uploadSetsButton.setEnabled(True)
        else:
            self.uploadSetsButton.setEnabled(False)
            self.generateManualButton.setEnabled(False)

    def _setInitialState(self):
        """ Set's initial state of the app by not allowing
        user to click on some buttons until value is entered
        for the number of rows. """
        self.rowNumber.clear()
        self.progressBar.setValue(0)
        self.uploadSetsButton.setEnabled(False)
        self.generateManualButton.setEnabled(False)
        self.uploadManualButton.setEnabled(True)
        self.closeButton.setEnabled(True)

    def _uploadManual(self):
        """ Reacts to user click on the 'Caricare Manuale button' """
        self.progressBar.setValue(0)
        self.manual_file_path = helper_functions.FileSelector().file_selector()
        if self.manual_file_path:
            msg_to_log = f'User ({helper_functions.get_user_name()}) - selected ' \
                         f'"{self.manual_file_path}" \nas input file for manual upload.'
            settings.LOGGER_CLS.log_info_msg(msg_to_log)
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
