import requests
import json
from django.conf import settings

class ZarinPalSandbox:

    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "http://127.0.0.1:8000/payment/verify/"

    def __init__(self, merchent_id=settings.MERCHENT_ID):
        self.merchent_id = merchent_id

    def payment_request(self, amount, description="پرداخت کاربر"):
        payload = {
            "merchent_id":self.merchent_id,
            "amount":int(amount),
            "callback_url": self._callback_url,
            "description":description
        }

        headers = {
            "Content-Type" : "application/json"
        }

        response = requests.post(self._payment_request_url, headers=headers, data=json.dump(payload))
        return response.json()

    def payment_verify(self, amount, authority_id):
        payload = {
            "merchent_id":self.merchent_id,
            "amount":int(amount),
            "authority_id":authority_id
        }

        headers = {
            "Content-Type":"application/json"
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=json.dump(payload))
        return response.json()

    def generate_payment_url(self, authority_id):
        return self._payment_page_url + authority_id
        