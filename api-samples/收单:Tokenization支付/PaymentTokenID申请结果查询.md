# PaymentTokenID申请结果查询 API Sample

## Request

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/InquireApplyRequest \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
  "version": "1.4",
  "keyVersion": "1",
  "requestTime": "2024-07-02T11:39:58.720+00:00",
  "appId": "d68f5da6a0174388821a64114c6b322c",
  "merchantNo": "P01010118267336",
  "data": {
    "userId": "ZHANGSAN",
    "tokenScope": "tokenAcq",
    "requestId": "DirectApi1716803778191"
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
