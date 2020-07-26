import json
import uuid
import hmac
import hashlib

import requests
from django.contrib import messages
from django.shortcuts import redirect
from home.models import Cart


def momo_payment(request,amoun):
    print(request.user)
    # parameters send to MoMo get get payUrl
    endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
    partnerCode = "MOMOPSQH20200627"
    accessKey = "ifNkJcHO7vkxo7HI"
    serectkey = "Qtni6MNmPj2aAvIjNU3CDGZBLJtHcWnu"
    orderInfo = "Pay for "+request.user.username+" Food"
    returnUrl = "http://localhost:8000/cart/paydone/"
    notifyurl = "http://localhost:8000/intro/"
    amount = str(int(amoun))
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "captureMoMoWallet"
    extraData = "merchantName=;merchantId="
    # pass empty value if your merchant does not have stores else merchantName=[storeName]; merchantId=[storeId] to identify a transaction map with a physical store
    rawSignature = "partnerCode=" + partnerCode + "&accessKey=" + accessKey + "&requestId=" + requestId + "&amount=" + amount + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&returnUrl=" + returnUrl + "&notifyUrl=" + notifyurl + "&extraData=" + extraData
    h = hmac.new(bytes(serectkey, 'latin-1'), bytes(rawSignature, 'latin-1'), digestmod=hashlib.sha256)
    signature = h.hexdigest()
    data = {
        'partnerCode': partnerCode,
        'accessKey': accessKey,
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'returnUrl': returnUrl,
        'notifyUrl': notifyurl,
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    data = json.dumps(data)
    clen = len(data)
    r = requests.post(endpoint, data, {'Content-Type': 'application/json', 'Content-Length': clen})
    wjson = json.dumps(r.json())
    print(r.json())
    if r.json()['errorCode']!= 0:
        messages.success(request,r.json()['localMessage'])
        return redirect('cart')
    return redirect(r.json()["payUrl"])
