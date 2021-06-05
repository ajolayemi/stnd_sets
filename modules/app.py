#!/usr/bin/env python

""" This module provides the STND_SETS application. """
import sys
from PyQt5.QtWidgets import QApplication
from views import UiWindow


def main():
    app = QApplication(sys.argv)
    win = UiWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
