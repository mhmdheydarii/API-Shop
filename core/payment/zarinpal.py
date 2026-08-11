import requests
import json
from django.conf import settings

class ZarinPalSandbox:

    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "http://127.0.0.1:8000/payment/verify-peyment/"

    def __init__(self, merchant_id=settings.MERCHANT_ID):
        self.merchant_id = merchant_id

    def payment_request(self, amount, description="پرداخت کاربر"):
        payload = {
            "merchant_id":self.merchant_id, 
            "amount":int(amount),
            "callback_url": self._callback_url,
            "description":description
        }

        headers = {
            "Content-Type" : "application/json"
        }

        response = requests.post(self._payment_request_url, headers=headers, data=json.dumps(payload))
        return response.json()

    def payment_verify(self, amount, authority_id):
        payload = {
            "merchant_id":self.merchant_id,
            "amount":int(amount),
            "authority":authority_id
        }

        headers = {
            "Content-Type":"application/json"
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=json.dumps(payload))
        return response.json()

    def generate_payment_url(self, authority_id):
        return self._payment_page_url + authority_id
        