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
                 db_name=DATABASE_NAME, con_name=CONNECTION_NAME,
                 table_name=TABLE_NAME):
        self.db_driver = db_driver
        self.db_name = db_name
        self.con_name = con_name
        self.table_name = table_name
        self.logger_cls = logger.Logger(file_name=LOG_FILE_NAME)

        self.con_error = False

        self._create_con()

    def populate_table(self, set_id: int, set_name: str,
                       set_component: str, component_qta: int,
                       component_netto_qta: int, component_id: int,
                       set_code: str):
        pass

    def create_table(self):
        table_query_cls = QSqlQuery(self.writer_connection)
        query = (
            f""" CREATE TABLE IF NOT EXISTS {self.table_name} (
            SetId INTEGER,
            SetName VARCHAR,
            SetComponent VARCHAR,
            ComponentQta FLOAT,
            ComponentQtaNetto FLOAT,
            ComponentID INTEGER,
            SetCode VARCHAR )
            """
        )
        table_query_cls.exec_(query)
        if table_query_cls.isActive():
            msg_to_log = f'{self.table_name} table was created successfully in \n' \
                         f'{self._get_db_name()}'
            self.logger_cls.log_info_msg(msg_to_log)
        else:
            msg_to_log = f'There was an error while trying to create {self.table_name} table in \n' \
                         f'{self._get_db_name()}'
            self.logger_cls.log_error_msg(msg_to_log)

    def _get_con_name(self):
        return self.writer_connection.connectionName()

    def _get_db_name(self):
        return self.writer_connection.databaseName()

    def _create_con(self):
        """ Creates database connection """
        self.writer_connection = QSqlDatabase.addDatabase(
            self.db_driver, connectionName=self.con_name
        )
        self.writer_connection.setDatabaseName(self.db_name)
        if not self.writer_connection.open():
            self.con_error = True
            msg_to_log = f'There was an error while trying to ' \
                         f'connect to database with writer connection name \n' \
                         f'{self.con_name}'
            self.logger_cls.log_error_msg(msg_to_log)
        else:
            msg_to_log = f'Writer connection - {self.con_name} - in DatabaseReader class created' \
                         f' successfully. '
            self.logger_cls.log_info_msg(msg=msg_to_log)


if __name__ == '__main__':
    t = DatabaseWriter()
    t.create_table()
