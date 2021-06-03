#!/usr/bin/env python

""" Reads data from database. """

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from settings import (DATABASE_NAME, TABLE_NAME,
                      CONNECTION_NAME, DATABASE_DRIVER,
                      LOG_FILE_NAME,
                      )

# helper_modules is a self defined module
from helper_modules import logger


class DatabaseWriter:

    def __init__(self, db_driver=DATABASE_DRIVER,
                 db_name=DATABASE_NAME, con_name=CONNECTION_NAME):
        self.db_driver = db_driver
        self.db_name = db_name
        self.con_name = con_name

        self.con_error = False

    def _create_con(self):
        """ Creates database connection """
        # Logger class
        logger_cls = logger.Logger(file_name=LOG_FILE_NAME)
        self.writer_connection = QSqlDatabase.addDatabase(
            self.db_driver, connectionName=self.con_name
        )
        self.writer_connection.setDatabaseName(self.db_name)
        if not self.writer_connection.open():
            self.con_error = True
            msg_to_log = f'Writer connection - {self.con_name} - in DatabaseReader class created' \
                         f'successfully. '
            logger_cls.log_info_msg(msg=msg_to_log)
        else:
            msg_to_log = f'There was an error while trying to create ' \
                         f'connect to database with writer connection name \n' \
                         f'{self.con_name}'
            logger_cls.log_error_msg(msg_to_log)
