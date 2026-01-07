# 纯API支付 API Sample

## Request

```bash
curl --request POST \
  --url 'https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay(for-auth-caputre-dont-copy-me)' \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
  "version": "1.4",
  "keyVersion": "1",
  "requestTime": "2022-02-25T09:23:06.473+00:00",
  "appId": "6666c8b036a24579974497c2f9800001",
  "merchantNo": "020213834421284",
  "data": {
    "outTradeNo": "Test1645780876511",
    "subject": "this is subject",
    "captureMode": "MANUAL",
    "authorizationType": "FINAL_AUTH",
    "totalAmount": 1,
    "currency": "AED",
    "country": "AE",
    "userId": "userId001",
    "integrate": "Direct_Payment",
    "expireTime": "1800",
    "paymentDetail": {
      "paymentMethodType": "CARD",
      "cardInfo": {
        "cardIdentifierNo": "4444333322221111",
        "cardHolderFullName": "James Smith",
        "cardExpirationMonth": "03",
        "cardExpirationYear": "30",
        "cvv": "123"
      },
      "buyerInfo": {
        "firstName": "James",
        "lastName": "Smith",
        "phoneNo": "903124360628",
        "email": "james@example.com",
        "clientIp": "124.156.108.193",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
      }
    },
    "goodsDetails": [
      {
        "goodsId": "D002",
        "goodsName": "Key buckle",
        "quantity": "2",
        "price": "0.5",
        "goodsCurrency": "AED",
        "showUrl": "http://xxx.example.com",
        "goodsCategory": "computer"
      }
    ],
    "shippingInfo": {
      "firstName": "James",
      "lastName": "Smith",
      "phoneNo": "903124360628",
      "email": "James@google.com",
      "address1": "GOLGELI SOKAK NO.34, 06700",
      "city": "GAZIOSMANPASA/ANKAR",
      "country": "TR",
      "zipCode": "06700"
    },
    "billingInfo": {
      "firstName": "James",
      "lastName": "Smith",
      "phoneNo": "903124360628",
      "email": "James@google.com",
      "address1": "GOLGELI SOKAK NO.34, 06700",
      "city": "GAZIOSMANPASA/ANKAR",
      "country": "TR",
      "zipCode": "06700"
    },
    "riskParams": {
      "registerName": "lily",
      "regTime": "2023-07-01 12:08:34",
      "liveCountry": "VN",
      "payerAccount": "987654XXX",
      "payerName": "lily",
      "taxId": "1234567890"
    },
    "language": "en",
    "reference": "020213827524152",
    "terminalType": "WAP",
    "frontCallbackUrl": "https://www.payermax.com",
    "notifyUrl": "https://www.payermax.com"
  }
}'
```

## Response

```json
{
  "code": "APPLY_SUCCESS",
  "msg": " Success.",
  "data": {
    "outTradeNo": "Test1645780876511",
    "tradeToken": "T2024062702289232000001",
    "status": "SUCCESS"
  }
}
```
