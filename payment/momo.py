import json
import uuid
import hmac
import hashlib

import requests
from django.shortcuts import redirect


def momo_payment():
    # parameters send to MoMo get get payUrl
    endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
    partnerCode = "MOMOPSQH20200627"
    accessKey = "ifNkJcHO7vkxo7HI"
    serectkey = "Qtni6MNmPj2aAvIjNU3CDGZBLJtHcWnu"
    orderInfo = "pay with MoMo"
    returnUrl = "http://localhost:8000/cart/paydone/"
    notifyurl = "http://localhost:8000/intro/"
    amount = "50000"
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "captureMoMoWallet"
    extraData = "merchantName=;merchantId="
    # pass empty value if your merchant does not have stores else merchantName=[storeName]; merchantId=[storeId] to identify a transaction map with a physical store
    rawSignature = "partnerCode=" + partnerCode + "&accessKey=" + accessKey + "&requestId=" + requestId + "&amount=" + amount + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&returnUrl=" + returnUrl + "&notifyUrl=" + notifyurl + "&extraData=" + extraData
    h = hmac.new(bytes(serectkey, 'latin-1'), bytes(rawSignature , 'latin-1'), digestmod=hashlib.sha256)
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
    clen=len(data)
    r=requests.post(endpoint,data,{'Content-Type': 'application/json', 'Content-Length': clen})
    wjson=json.dumps(r.json())
    print(r.json()["payUrl"])
    return redirect(r.json()["payUrl"])