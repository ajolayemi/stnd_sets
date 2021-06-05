""" Contains various worker threads used in this project. """

from PyQt5.QtCore import QObject, pyqtSignal

# Self defined modules
import excel_communicator
from database_writer import DatabaseWriter
from helper_modules import helper_functions, logger
import settings


class SetUploader(QObject):
    # Custom signals
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    unfinished = pyqtSignal()

    def __init__(self, file_path: str, row_num: int):
        super(SetUploader, self).__init__()
        self._file_path = file_path
        self._row_num = int(row_num)

    def setUploader(self):
        data_worksheet = excel_communicator.load_worksheet_by_index(
            self._file_path, settings.SET_SHEET
        )
        worksheet_log = f'Worksheet ({data_worksheet}) at index {settings.SET_SHEET} in {self._file_path}' \
                        f'\nloaded successfully'
        settings.LOGGER_CLS.log_info_msg(worksheet_log)
        db_cls = DatabaseWriter()
        db_cls.create_con()
        db_cls.create_table()

        for row_index in range(2, self._row_num + 1):
            set_id = excel_communicator.get_info(data_worksheet, row_index, 1)
            set_name = helper_functions.name_controller(
                name=excel_communicator.get_info(data_worksheet, row_index, 2),
                char_to_remove='"')
            set_component = excel_communicator.get_info(data_worksheet, row_index, 3)
            component_qta = excel_communicator.get_info(data_worksheet, row_index, 4)
            component_net_qta = excel_communicator.get_info(data_worksheet, row_index, 5)
            component_id = excel_communicator.get_info(
                data_worksheet, row_index, 6
            )
            set_code = excel_communicator.get_info(data_worksheet, row_index, 7)

            self.progress.emit(helper_functions.get_percentage_of(row_index, self._row_num))

            table_writer = db_cls.populate_table(
                set_id, set_name, set_component, component_qta,
                component_net_qta, component_id, set_code
            )

        self.progress.emit(0)
        if table_writer[0]:
            self.logger_cls.log_info_msg(table_writer[1])
            self.finished.emit()
            self.logger_cls.close()
        else:
            self.logger_cls.log_error_msg(table_writer[1])
            self.unfinished.emit()
            self.logger_cls.close()


