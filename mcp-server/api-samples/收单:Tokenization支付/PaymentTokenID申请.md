# PaymentTokenID申请 API Sample

## Request

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/applyPaymentToken \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
  "version": "1.4",
  "keyVersion": "1",
  "requestTime": "2024-07-02T11:39:58.720+00:00",
  "appId": "d68f5da6a01766666621a64114c6b322c",
  "merchantNo": "P01011118267336",
  "data": {
    "requestId": "DirectApi1718074257802",
    "country": "RU",
    "paymentMethodType": "CARD",
    "targetOrg": null,
    "userId": "052718",
    "frontCallbackUrl": "https://www.frontcallbackurl.example.com",
    "tokenScope": "tokenAcq",
    "mitType": "UNSCHEDULE",
    "cardInfo": {
      "cardOrg": "VISA",
      "cardIdentifierNo": "4444333322221111",
      "cardHolderFullName": "James Smith",
      "cardExpirationMonth": "03",
      "cardExpirationYear": "30",
      "cvv": "123"
    },
    "envInfo": {
      "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
      "clientIp": "12.233.22.213",
      "terminalType": "app",
      "osType": "ios",
      "osVersion": "15.5",
      "browserType": "",
      "timeZone": "",
      "deviceId": "eYOIkvFpZzztg00Yu6USdprBQZCWxDhiUAHCiK&K/cH9mT6wMaMOzAKe",
      "deviceLanguage": "zh_CN",
      "screenHeight": "768",
      "screenWidth": "1024"
    },
    "riskParams": {
      "accountNo": "xsxxx",
      "bindEmail": "xx@example.com",
      "regTime": "2024-03-14 12:08:34"
    }
  }
}'
```

## Response

```json
{
  "msg": "",
  "code": "APPLY_SUCCESS",
  "data": {
    "redirectUrl": "https://cashier-n-test-new.payermax.com/index.html#/paySDKH5/newAuthResultSimulator?pmaxUrlMock=1&notifyType=CONTROL&referenceNo=TUC858400171807425915435000029&frontCallbackURL=http://baidu.com",
    "requestId": "DirectApi1718074257802",
    "status": "PENDING"
  }
}
```
