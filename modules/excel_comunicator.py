
""" Handles communication with excel files. """
import openpyxl
import xlsxwriter.exceptions
import os
from settings import (COLUMNS_LIST,
                      OUTPUT_FILE_NAME,
                      OUTPUT_SHEET_NAME)
import xlrd

# helper_modules is a self defined module
from helper_modules import logger

import string

ALPHA_UPPER = list(string.ascii_uppercase)


def create_output_file(file_name=OUTPUT_FILE_NAME,
                       sheet_name=OUTPUT_FILE_NAME) -> bool:
    """ Creates an excel file that will serve as file where output
    data will be written. """
    output_workbook = openpyxl.Workbook()
    active_sheet = output_workbook.active
    active_sheet.title = sheet_name
    for index, col_name in enumerate(COLUMNS_LIST, 1):
        active_sheet[f'{ALPHA_UPPER[index]}1'] = COLUMNS_LIST[index - 1]
    output_workbook.save(filename=file_name)
    return os.path.exists(file_name)


def write_to_output_file(client_info: str, set_ordered: str,
                         set_ordered_id: int, set_component: str,
                         set_component_id: str, total_qta: int,
                         workbook: openpyxl.workbook.Workbook,
                         worksheet: openpyxl.worksheet.worksheet.Worksheet) -> tuple[bool, str]:
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


def load_output_file(file_path=OUTPUT_FILE_NAME,
                     sheet_name=OUTPUT_SHEET_NAME) -> tuple:
    file_creator = create_output_file()
    if file_creator:
        output_workbook = openpyxl.load_workbook(file_path)
        output_worksheet = output_workbook[sheet_name]
        return True, output_workbook, output_worksheet
    else:
        return False, False, False
