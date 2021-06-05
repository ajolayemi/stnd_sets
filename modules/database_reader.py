#!/usr/bin/env python

""" Reads data from database. """

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from collections import namedtuple

# Self defined modules
from settings import (DATABASE_NAME, TABLE_NAME,
                      READER_CON_NAME, DATABASE_DRIVER,
                      LOG_FILE_NAME, LOGGER_CLS)
from helper_modules import logger


class DatabaseReader:
    """ Reads data from database """

    def __init__(self, db_driver=DATABASE_DRIVER, db_name=DATABASE_NAME,
                 con_name=READER_CON_NAME, table_name=TABLE_NAME):
        self.db_driver = db_driver
        self.db_name = db_name
        self.con_name = con_name
        self.table_name = table_name

        self.con_error = False

        self.reader_connection = None

    def drop_table(self):
        delete_query = QSqlQuery(self.reader_connection)
        delete_query.exec(f'DROP TABLE {self.table_name}')
        if delete_query.isActive():
            msg_to_log = f'{self.table_name} table in {self.db_name} was' \
                         f' successfully deleted.'
            LOGGER_CLS.log_info_msg(msg_to_log)

        else:
            msg_to_log = f'Attempt to delete {self.table_name} table in ' \
                         f'{self.db_name} failed.'
            LOGGER_CLS.log_error_msg(msg_to_log)

    def table_is_empty(self):
        """ Checks to see if table is empty, returns True if it is empty
        False otherwise. """
        check_query = QSqlQuery(self.reader_connection)
        query = f'SELECT * FROM {self.table_name}'
        check_query.exec(query)
        empty_table = check_query.first()
        check_query.finish()
        return not empty_table

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
                if not any((component_id == '', component_qta == '', component_netto_qta == '')):
                    components_det[component] = DetTuple(component_id, component_qta,
                                                         component_netto_qta)
            components_query.finish()
            return components_det
        else:
            components_query.finish()
            msg_to_log = f'Attempt to retrieve set components of ID: {set_id} failed'
            LOGGER_CLS.log_error_msg(msg_to_log)
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

    def create_reader_con(self):
        self.reader_connection = QSqlDatabase.addDatabase(
            self.db_driver, connectionName=self.con_name
        )
        self.reader_connection.setDatabaseName(self.db_name)
        if not self.reader_connection.open():
            msg_to_log = f'There was an error while trying to ' \
                         f'connect to database with reader connection name \n' \
                         f'{self.con_name}.'
            LOGGER_CLS.log_error_msg(msg_to_log)
            self.con_error = True
        else:
            msg_to_log = f'Reader connection - {self.con_name} - in DatabaseReader class created' \
                         f' successfully.'
            LOGGER_CLS.log_info_msg(msg=msg_to_log)


if __name__ == '__main__':
    pass
