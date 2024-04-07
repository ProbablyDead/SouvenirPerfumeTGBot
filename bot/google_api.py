import gspread
import os 
import zoneinfo

from datetime import datetime
from dotenv import load_dotenv

from tele_test import INGREDIENT_QUESTION_COUNT

from operator import add
from functools import reduce

load_dotenv()

EMPTY_USER = "__empty__"
CREDENTIALS_FILE = './secrets/creds.json' 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
if not SPREADSHEET_ID:
    print("No spreadsheet id")
    exit()

class Google_worker:
    def __init__(self) -> None:
        self._gc = gspread.service_account(filename=CREDENTIALS_FILE)
        self._sh = self._gc.open_by_key(SPREADSHEET_ID)
        self._worksheet = self._sh.get_worksheet_by_id(0)

    def get_body(self, values):
        body = list(filter(lambda x: x is not None,
                           reduce(add, [ value if value.__class__ == list  
                                        else [value] for value in values.values()])))

        return body

                    
    def update_sheet(self, userName: str, new_values) -> None:
        cell = self._worksheet.find(userName)
        body = self.get_body(new_values)

        if cell:
            self._worksheet.update(range_name=cell.address,
                                   values=[body])
        else:
            self._add_line(body)

    def add_payment(self, userName, new_value):
        cell = self._worksheet.find(userName)

        payment_cell_col = cell.col + INGREDIENT_QUESTION_COUNT + 3

        zone = zoneinfo.ZoneInfo("Europe/Moscow")

        self._worksheet.update_cell(cell.row, payment_cell_col, new_value)
        self._worksheet.update_cell(cell.row, payment_cell_col + 1, 
                                    str(datetime.now(zone).date()))
        self._worksheet.update_cell(cell.row, payment_cell_col + 2, 
                                    datetime.now(zone).time().strftime("%H:%M:%S"))

    def _add_line(self, body) -> None:
        self._worksheet.append_row(body, table_range='A:A')

