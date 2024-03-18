import gspread
import os

from dotenv import load_dotenv

from operator import add
from functools import reduce

load_dotenv()

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
        return list(filter(lambda x: x is not None, reduce(add, [ value if value.__class__ == list  else [value] for value in values.values()])))

                    
    def update_sheet (self, userName: str, new_values) -> None:
        cell = self._worksheet.find(userName)
        if cell:
            self._worksheet.update(range_name=cell.address, values=[self.get_body(new_values)])
        else:
            self._add_line(new_values)


    def _add_line(self, value) -> None:
        self._worksheet.append_row(self.get_body(value), table_range='A:A')

