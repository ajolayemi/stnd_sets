
"""" Holds various variables and constants used in this project. """
from helper_modules import helper_functions

STRING = f'output {helper_functions.get_user_name()}'
OUTPUT_FILE_NAME = f'{STRING}.xlsx'
OUTPUT_SHEET_NAME = 'Output'

# Database constants
DATABASE_NAME = 'DBProdotti.sqlite'
TABLE_NAME = 'SETS'
CONNECTION_NAME = 'Writer'
DATABASE_DRIVER = 'QSQLITE'
READER_CON_NAME = 'Reader'


# Output file column constants
COLUMN_1_TITLE = "n° ordine - nome cliente - id prod"
COLUMN_2_TITLE = "Nome MIX STND ordinato"
COLUMN_3_TITLE = "ID MIX STND"
COLUMN_4_TITLE = "Componente MIX STND"
COLUMN_5_TITLE = "ID Componente MIX STND"
COLUMN_6_TITLE = "Qtà Totale"


COLUMNS_LIST = [COLUMN_1_TITLE, COLUMN_2_TITLE,
                COLUMN_3_TITLE, COLUMN_4_TITLE,
                COLUMN_5_TITLE, COLUMN_6_TITLE]
