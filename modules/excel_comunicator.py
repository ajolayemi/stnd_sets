
""" Handles communication with excel files. """
import openpyxl
import xlsxwriter.exceptions

from settings import (COLUMNS_LIST,
                      OUTPUT_FILE_NAME,
                      OUTPUT_SHEET_NAME)
import xlrd

# helper_modules is a self defined module
from helper_modules import logger


def write_to_output_file(client_info: str, set_ordered: str,
                         set_ordered_id: int, set_component: str,
                         set_component_id: str, total_qta: int,
                         workbook: openpyxl.workbook.Workbook,
                         worksheet: openpyxl.worksheet.worksheet.Worksheet):
    """ Writes to output_file """
    try:
        worksheet.append([client_info, set_ordered, set_ordered_id,
                          set_component, set_component_id, total_qta])
        worksheet.title = OUTPUT_SHEET_NAME
        workbook.save(OUTPUT_FILE_NAME)
        return True, f'Data written in {OUTPUT_FILE_NAME} successfully'
    except PermissionError:
        return False, f'{OUTPUT_FILE_NAME} file was open'
    except ValueError:
        return False, f'The requested sheet was not found'
    except (NameError, FileNotFoundError):
        return False, f'The requested workbook or excel file does not' \
                      f'exist'
    except (KeyError, xlrd.biffh.XLRDError,
            xlsxwriter.exceptions.FileCreateError):
        return False, 'Other un-handled errors occurred'
