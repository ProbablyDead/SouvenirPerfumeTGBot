import shelve
from tele_test import QUESTION_COUNT

class Database:
    PATH = "data/data"

    def __init__(self) -> None:
        self.database = shelve.open(self.PATH, writeback=True)


    def create_db_str(self, id):
        self.database[str(id)] = [None] * QUESTION_COUNT
    
    
    def update_db_str(self, id, at: int, ans: str):
        s_id = str(id)
        s = self.database[s_id]
        s[at] = ans
        self.database[s_id] = s
    
    
    def get_db_str(self, id):
        return self.database.get(str(id), [])

