import requests
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect
from .messaging import get_message
from django.contrib import messages
import json

_data = {
    'MERCHANT': '',
    "ZP_API_REQUEST": "https://api.zarinpal.com/pg/v4/payment/request.json",
    "ZP_API_VERIFY": "https://api.zarinpal.com/pg/v4/payment/verify.json",
    "ZP_API_STARTPAY": "https://www.zarinpal.com/pg/StartPay/{authority}",
    "description": "توضیحات مربوط به تراکنش را در این قسمت وارد کنید",
    "CallbackURL": 'http://{domain}/verify_payment/{amount}/{payment_type}/'
}


def send_request(method, url, data):
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    return requests.request(method, url, headers=headers, data=json.dumps(data)).json()


def start_payment(request, amount, payment_type):
    req_data = {
        "merchant_id": _data['MERCHANT'],
        "amount": amount,
        "callback_url": _data['CallbackURL'].format(
            amount=amount,
            payment_type=payment_type,
            domain=get_current_site(request).domain
        ),
        "description": _data['description']
    }
    response = send_request('POST', _data['ZP_API_REQUEST'], req_data)
    print(response)
    authority = response['data']['authority']
    if not response['errors']:
        return redirect(_data['ZP_API_STARTPAY'].format(authority=authority))
    else:
        e_code = response['errors']['code']
        e_message = response['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify_payment(request, amount, payment_type):
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_data = {
            "merchant_id": _data['MERCHANT'],
            "amount": amount,
            "authority": t_authority
        }
        response = send_request('POST', _data['ZP_API_VERIFY'], req_data)
        if len(response['errors']) == 0:
            t_status = response['data']['code']
            if t_status == 100:
                if payment_type == 'credit':
                    request.user.add_credit(int(amount))
                    messages.add_message(request, messages.SUCCESS, get_message('authentication/credit_added'))
                    return redirect('profile')
                else:
                    try:
                        order = request.user.orders.get(is_paid=False)
                        order.process_order()
                        messages.add_message(request, messages.SUCCESS, get_message('orders/order_submitted'))
                        return redirect('user_orders')
                    except AttributeError:
                        raise

            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    response['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    response['data']['message']
                ))
        else:
            e_code = response['errors']['code']
            e_message = response['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')
