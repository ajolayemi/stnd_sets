#!/usr/bin/env python

""" Reads data from database. """

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# Self defined modules
from settings import (DATABASE_NAME, TABLE_NAME,
                      READER_CON_NAME, DATABASE_DRIVER,
                      LOG_FILE_NAME)
from helper_modules import logger


class DatabaseReader:
    """ Reads data from database """

    def __init__(self, db_driver=DATABASE_DRIVER, db_name=DATABASE_NAME,
                 con_name=READER_CON_NAME, table_name=TABLE_NAME):
        self.db_driver = db_driver
        self.db_name = db_name
        self.con_name = con_name
        self.table_name = table_name

        self.logger_cls = logger.Logger(file_name=LOG_FILE_NAME)

        self.con_error = False

        self._create_con()

    @staticmethod
    def _get_active_cons():
        return QSqlDatabase.connectionNames()

    def _get_tables_in_db(self):
        return self.reader_connection.tables()

    def _get_con_name(self):
        return self.reader_connection.connectionName()

    def _create_con(self):
        self.reader_connection = QSqlDatabase.addDatabase(
            self.db_driver, connectionName=self.con_name
        )
        self.reader_connection.setDatabaseName(self.db_name)
        if not self.reader_connection.open():
            msg_to_log = f'There was an error while trying to ' \
                         f'connect to database with reader connection name \n' \
                         f'{self.con_name}\n\n'
            self.logger_cls.log_error_msg(msg_to_log)
            self.con_error = True
        else:
            msg_to_log = f'Reader connection - {self.con_name} - in DatabaseReader class created' \
                         f' successfully.\n\n'
            self.logger_cls.log_info_msg(msg=msg_to_log)


if __name__ == '__main__':
    t = DatabaseReader()
