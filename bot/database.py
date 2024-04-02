import shelve
import os

from tele_test import QUESTION_COUNT
from google_api import Google_worker

PATH = os.getenv('DATA_PATH')

if PATH is None:
    print("Cannot locate env var DATA_PATH")
    exit(1)


class Database:
    QUESTIONS = "questions"
    USER_NAME = "userName"
    PASS_COUNT = "passCount"
    PAYMENT_COUNT = "payments"

    def __init__(self) -> None:
        self.database = shelve.open(PATH + "data", writeback=True)
        self.EMPTY_ARR = [None] * QUESTION_COUNT
        self.google_worker = Google_worker()

    def clean_db_question_array(self, id):
        s = self.database[str(id)]
        self.database[str(id)] = {self.USER_NAME: s[self.USER_NAME],
                                  self.QUESTIONS: [None]*9,
                                  self.PASS_COUNT: s[self.PASS_COUNT],
                                  self.PAYMENT_COUNT: s[self.PAYMENT_COUNT] if
                                    self.PAYMENT_COUNT in s else 0
                                  }

    def create_db_str(self, id, userName):
        if str(id) in self.database:
            self.clean_db_question_array(id)
        else:
            self.database[str(id)] = {
                    self.USER_NAME: userName, self.QUESTIONS:
                    self.EMPTY_ARR.copy(), self.PASS_COUNT: 0,
                    self.PAYMENT_COUNT: 0
                    }

    def update_db_question_array(self, id, at: int, ans: str):
        self.database[str(id)][self.QUESTIONS][at] = ans

    def get_db_question_array_after_complete(self, id):
        st = self.database.get(str(id), {self.QUESTIONS: [],
                                         self.PASS_COUNT: 0,
                                         self.PAYMENT_COUNT: 0
                                         })
        st[self.PASS_COUNT] += 1
        self.google_worker.update_sheet(st[self.USER_NAME], st)
        return st[self.QUESTIONS]

    def get_db_user_name(self, id):
        return self.database[str(id)][self.USER_NAME]

    def get_db_str(self, id):
        return self.database.get(str(id), {})

    def get_db_pass_count(self, id):
        return self.database.get(str(id),
                                 {self.PASS_COUNT: 0})[self.PASS_COUNT]

    def get_db(self) -> list:
        return [(key, value) for key, value in self.database.items()]

    def del_db_item(self, id):
        del self.database[str(id)]

    def add_db_payment(self, id):
        st = self.database.get(str(id), {self.QUESTIONS: [],
                                         self.PASS_COUNT: 0,
                                         self.PAYMENT_COUNT: 0
                                         })
        st[self.PAYMENT_COUNT] += 1
        self.google_worker.add_payment(st[self.USER_NAME], st[self.PAYMENT_COUNT])

    def __del__(self) -> None:
        self.database.close()
