import os
import json
import time
import threading
from dotenv import load_dotenv

from yookassa import Configuration, Payment as pmt

load_dotenv()

SHOP_ID = os.getenv('SHOP_ID')
SHOP_KEY = os.getenv('SHOP_KEY')

Configuration.configure(SHOP_ID, SHOP_KEY)

PRICE = os.getenv('PRICE')
RETURN_URL = os.getenv('RETURN_URL')

def test(succeed, username):
    print(succeed)

class Payment:
    def __init__(self):
        self._DESCRIPTION = "description"
        self._payment_id = None

    def create_payment(self, callback, customer_tg_username):
        payment = pmt.create({
            "amount": {
                "value": PRICE,
                "currency": "RUB"
                },
            "payment_method_data": {
                "type": "bank_card"
                },
            "confirmation": {
                "type": "redirect",
                "return_url": RETURN_URL
                },
            "capture": True,
            "description": self._DESCRIPTION
            })
        
        payment_data = json.loads(payment.json())
        self._payment_id = payment_data['id']

        # Run in parallel thread
        threading.Thread(target=self._check_payment, 
                         args=(callback,customer_tg_username)).start()

        return (payment_data['confirmation'])['confirmation_url']

    # callback - (bool) => None
    def _check_payment(self, callback, customer_tg_username):
        payment = json.loads((pmt.find_one(self._payment_id)).json())
        while payment['status'] == 'pending':
            payment = json.loads((pmt.find_one(self._payment_id)).json())
            time.sleep(3)

        callback(payment['status'] == 'succeeded', customer_tg_username)


print(Payment().create_payment(test, 'yakiza'))

while True:
    pass

