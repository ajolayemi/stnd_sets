#!/usr/bin/env python

""" Reads data from database. """

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# Self defined modules
from settings import (DATABASE_NAME, TABLE_NAME,
                      READER_CON_NAME, DATABASE_DRIVER,
                      LOG_FILE_NAME)
from helper_modules import logger
