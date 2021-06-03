#!/usr/bin/env python

""" Reads data from database. """

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from collections import namedtuple

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

    def check_table(self):
        """ Checks to see if table is empty, returns True if it is empty
        False otherwise. """
        check_query = QSqlQuery(self.reader_connection)
        query = f'SELECT * FROM {self.table_name}'
        check_query.exec(query)
        return not check_query.first()

    def get_set_components_det(self, set_id: int):
        """ Returns a dict where the keys are the components
        of a set and values are a named tuple containing component id,
        component_qta, component_net_qta. """
        components_det = {}
        DetTuple = namedtuple('DetTuple',
                              ['component_id', 'component_qta',
                               'component_netto_qta'])
        components_query = QSqlQuery(self.reader_connection)
        query = f'SELECT SetComponent, ComponentID, ComponentQta,' \
                f'ComponentQtaNetto FROM {self.table_name} WHERE ' \
                f'SetId = {set_id}'
        if components_query.prepare(query):
            components_query.exec()
            while components_query.next():
                component = components_query.value(
                    components_query.record().indexOf('SetComponent'))
                component_id = components_query.value(
                    components_query.record().indexOf('ComponentID')
                )
                component_qta = components_query.value(
                    components_query.record().indexOf('ComponentQta'))
                component_netto_qta = components_query.value(
                    components_query.record().indexOf('ComponentQtaNetto'))
                components_det[component] = DetTuple(component_id, component_qta,
                                                     component_netto_qta)
            components_query.finish()
            return components_det
        else:
            components_query.finish()
            msg_to_log = f'Attempt to retrieve set components of ID: {set_id} failed'
            self.logger_cls.log_error_msg(msg_to_log)
            return {}

    def get_set_name(self, set_id):
        """ Retrieves the name of a given set_id"""
        name_query = QSqlQuery(self.reader_connection)
        query = f'SELECT SetName FROM {self.table_name} ' \
                f'WHERE SetId = {set_id}'

        if name_query.prepare(query):
            name_query.exec(query)
            set_name_index = name_query.record().indexOf("SetName")
            name_query.first()
            set_name = name_query.value(set_name_index)
            name_query.finish()
            return set_name, True
        else:
            name_query.finish()
            return None, False

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
    print(t.check_table())
