import requests
from django.conf import settings
import json

class Paystack:
    base_url = 'https://api.paystack.co'

    def confirm_payment(self, reference):
        headers= {
            "Authorization": f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        }
        res = requests.get(self.base_url+f'/transaction/verify/{reference}',
                            headers=headers)

        return res.json()['data']
