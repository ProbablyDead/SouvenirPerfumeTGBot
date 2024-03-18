import gspread

from operator import add
from functools import reduce

CREDENTIALS_FILE = './secrets/creds.json' 
SPREADSHEET_ID = '13-aF48VaqhR34DAHhNoUyQ8__qtq-640fThVKbehbzo'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

class Google_worker:
    def __init__(self) -> None:
        self._gc = gspread.service_account(filename=CREDENTIALS_FILE)
        self._sh = self._gc.open_by_key(SPREADSHEET_ID)
        self._worksheet = self._sh.get_worksheet_by_id(0)

    def get_body(self, values):
        return reduce(add, [ value if value and value.__class__ == list  else [value] for value in values.values()])

                    
    def updete_row (self, userName: str, new_values) -> None:
        cell = self._worksheet.find(userName)
        if cell:
            self._worksheet.update(range_name=cell.address, values=[self.get_body(new_values)])


    def add_line(self, value) -> None:
        self._worksheet.append_row(self.get_body(value), table_range='A:A')



w = Google_worker()
w.updete_row('yakiza', { "user": "yakiza", "QUESTIONS": ["a fs", "as jkdjaf f", "aaaaaa"], "PASS_COUNT": 2 })

w.add_line({ "user": "yakiza", "QUESTIONS": ["a fs", "as jkdjaf f", "aaaaaa"], "PASS_COUNT": 1 })
