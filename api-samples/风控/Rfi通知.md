# Rfi通知 API Sample

## Request

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/rfiNotifyUrl \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
  "keyVersion": "1",
  "notifyTime": "2023-10-20T03:28:23.092Z",
  "appId": "{{appId}}",
  "merchantNo": "{{merchantNo}}",
  "data": {
    "rfiNo": "testRFINo001",
    "remark": "test",
    "businessType": "PAYMENT",
    "status": "REVIEW",
    "relateOrderId": [
      "order0001"
    ],
    "materialList": [
      {
        "fieldName": "ID",
        "fieldType": "file"
      }
    ],
    "expireTime": "2023-10-20T03:28:23.092Z"
  }
}'
```

## Response

```json
{
  "code": "string",
  "msg": "string"
}
```
