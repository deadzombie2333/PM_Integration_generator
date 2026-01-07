# Apply Drop-in Session API Sample

## Request

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/applyDropinSession \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
  "version": "1.1",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "3b242b56a8b64274bcc37dac281120e3",
  "merchantNo": "020213827212251",
  "data": {
    "currency": "IDR",
    "country": "ID",
    "userId": "U10001",
    "tokenForFutureUse": false,
    "componentList": [
      "CARD",
      "APPLEPAY"
    ]
  }
}'
```

## Response

```json
{
  "code": "APPLY_SUCCESS",
  "msg": "Success.",
  "data": {
    "clientKey": "37114858239eur2384237r810482390",
    "sessionKey": "bdsf8982348974hhf82934bf8239424"
  }
}
```
