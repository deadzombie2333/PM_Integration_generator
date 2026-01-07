# paymentTokenID查询 API Sample

## Request

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/inquirePaymentToken \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
  "version": "1.2",
  "keyVersion": "1",
  "requestTime": "2022-01-22T10:00:00.500+08:00",
  "appId": "46153e2b787241ae8b01857bb087d1bd",
  "merchantNo": "010229810189301",
  "data": {
    "userId": "TEST",
    "tokenScope": "tokenAcq",
    "paymentTokenID": "PMTOKEN20230424072005899168200035002",
    "paymentMethodType": "CARD",
    "cardOrg": "VISA",
    "referralCode": "xxx"
  }
}'
```

## Response

```json
{
  "msg": "",
  "code": "APPLY_SUCCESS",
  "data": {
    "tokenList": [
      {
        "tokenScope": "tokenAcq",
        "targetOrg": "",
        "ifCVV": "N",
        "cardInfo": "455701******1010",
        "paymentTokenID": "PMTOKEN20230710080439571142400031000",
        "accountDisplay": "",
        "paymentTokenStatus": "Activated",
        "userId": "czy_0088",
        "brand": "VISA",
        "paymentMethodType": "CARD",
        "paymentTokenExpiry": "2023-07-14T00:00:00.537Z",
        "referralCode": "xxxx"
      }
    ]
  }
}
```
