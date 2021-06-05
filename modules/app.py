#!/usr/bin/env python

""" This module provides the STND_SETS application. """
import sys
from PyQt5.QtWidgets import QApplication
from views import UiWindow
from helper_modules import helper_functions
from settings import LOGGER_CLS, LOG_FILE_NAME

with open(LOG_FILE_NAME, 'a') as file:
    file.write(f'\n {"-" * 130}\n')


def main():
    LOGGER_CLS.log_info_msg(f'User ({helper_functions.get_user_name()}) started a new '
                            f'session.')
    app = QApplication(sys.argv)
    win = UiWindow()
    win.show()
    exit_code = app.exec_()
    if exit_code == 0:
        msg_to_log = 'App exited with exit code of 0. Successful operations.'
        LOGGER_CLS.log_info_msg(msg_to_log)
    else:
        msg_to_log = 'App exited with exit code other than 0. Unsuccessful operations'
        LOGGER_CLS.log_error_msg(msg_to_log)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
