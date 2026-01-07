# 收单/纯API支付 (Direct API Payment)

## API Information

- **Method**: POST
- **Endpoint**: `https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay`
- **Content-Type**: `application/json`

## Description

商户希望在自己的收银台上给用户展示支付方式并支付，PayerMax提供纯API（Direct API）的方式接入。

**重要提示**：
- 对于Direct API的接口，商户如果自行处理卡号信息，需要具备PCI-DSS认证资质
- 商户如果换汇或营销的诉求，可联系PayerMax技术支持

## Request Headers

| Header | Type | Required | Description | Example |
|--------|------|----------|-------------|---------|
| Content-Type | string | ✓ | Request content type | `application/json` |
| sign | string | ✓ | 签名信息请参考技术文档 | `FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==` |

## Request Body Parameters

### Root Level Parameters

| Parameter | Type | Required | Max Length | Description |
|-----------|------|----------|------------|-------------|
| version | string | ✓ | 8 | 接口版本 当前值为：1.4 |
| keyVersion | string | ✓ | 8 | 密钥版本 当前值为：1 |
| requestTime | string | ✓ | 32 | 请求时间，符合rfc3339规范，格式：yyyy-MM-dd'T'HH:mm:ss.SSSXXX 时间需要在当前时间两分钟内 |
| appId | string | ✓ | 64 | 商户应用Id，PayerMax分配给商户应用的唯一标识 |
| merchantNo | string | ✗ | 32 | 商户号，商户与PayerMax业务签约时生成的唯一标识 |
| data | object | ✓ | - | 请求数据体 |

### Data Object Parameters

| Parameter | Type | Required | Max Length | Description |
|-----------|------|----------|------------|-------------|
| outTradeNo | string | ✓ | 64 | 商户订单号，唯一标识商户的一笔交易，不能重复，只能包含字母、数字、下划线且不支持大小写敏感。如：AAA和AAa被认为是相同的。 |
| integrate | string | ✓ | 16 | 商户自行进行付款方支付信息的收集后，传送给PayerMax进行交易处理,需传入参数：**Direct_Payment** |
| subject | string | ✓ | 256 | 订单标题或产品信息，会展示在用户支付页面，避免使用纯数字。注：巴西钱包Pix不能超过43位 |
| totalAmount | number | ✓ | - | 标价金额，金额的单位为元。各个国家币种支持的小数位详见【交易支持国家/地区与币种】,风控限额详见【风控行业限额】 |
| currency | string | ✓ | 3 | 标价币种，大写字母，参见【交易支持国家/地区与币种】 |
| country | string | ✓ | 2 | 国家代码，大写字母，参见【交易支持国家/地区与币种】 |
| userId | string | ✓ | 64 | 商户内部的用户Id，需要保证每个ID唯一性。 |
| terminalType | string | ✓ | 3 | 设备终端，WEB，WAP，APP |
| paymentDetail | object | ✓ | - | 支付信息 |
| expireTime | string | ✗ | - | 指定关单时间(单位：秒)。最小30分钟，最大1天。若传入则以该时间为关单时间。默认30分钟 |
| referralCode | string | ✗ | 32 | 用于更精准的支付方式推荐，如设备ID、设备指纹等。 |
| mitManagementUrl | string | ✗ | - | 商户订阅管理页面地址 |
| subscriptionPlan | object | ✗ | - | 订阅计划信息 |
| goodsDetails | array[object] | ✗ | - | 商品信息，支持传多个。注：电商场景下需要上送。如果传入该对象，则内层必填字段必须传入 |
| subMerchant | object | ✗ | - | 二级商户信息 平台类商户需要上送子商户信息 |
| shippingInfo | object | ✗ | - | 邮寄信息。注：电商场景下需要上送。如果传入该对象，则内层必填字段必须传入 |
| billingInfo | object | ✗ | - | 信用卡账单地址信息。注：如果传入该对象，则内层必填字段必须传入 |
| envInfo | object | ✗ | - | 设备信息 |
| language | string | ✗ | 16 | 收银台页面语言。【支持的国家与币种】优先级：用户上次使用的语言 > 用户浏览器语言 > 用户ip国家语言 > 商户下单传的语言 > 默认EN |
| riskParams | object | ✗ | - | 详见风控业务数据：【商户上送信息】，该部分信息通常作为定制风控的补充信息，如未开通定制风控可不填。 |
| osType | string | ✗ | - | 设备操作系统，当设备终端为Wap和App时，设备操作系统可以为ANDROID或IOS |
| reference | string | ✗ | 512 | 商户自定义附加数据，可支持商户自定义并在响应中返回 |
| frontCallbackUrl | string | ✗ | 1024 | 商户指定的跳转URL，用户完成支付后会被跳转到该地址，以http/https开头或者商户应用的scheme地址，纯API支付下frontCallbackUrl是必填的，用于支持需要跳转外部的异步交易 |
| notifyUrl | string | ✗ | 256 | 服务端回调通知URL，以http/https开头 可以通过MerchantDashboard平台配置商户通知地址，详情见【配置异步通知地址】，如果交易中上送，则以交易为准，即优先使用接口中传的url。注：如商户平台未配置通知地址，交易也没上送地址，则无法进行回调通知 |

## Response (200)

### Response Body

| Parameter | Type | Required | Max Length | Description |
|-----------|------|----------|------------|-------------|
| code | string | ✓ | - | 返回码，'APPLY_SUCCESS'代表成功。只代表接口请求成功，不代表订单状态。 |
| msg | string | ✓ | - | 返回描述，'Success.'。只代表接口请求成功，不代表订单状态。 |
| data | object | ✗ | - | 返回数据体 |

### Data Object (Response)

| Parameter | Type | Required | Max Length | Description |
|-----------|------|----------|------------|-------------|
| outTradeNo | string | ✓ | 64 | 商户订单号 |
| tradeToken | string | ✓ | 64 | PayerMax流水号 |
| status | string | ✓ | 32 | 交易状态，详见【交易状态】 |
| redirectUrl | string | ✗ | 1024 | 跳转地址 部分支付方式需要跳转外部完成支付 |

## Key Differences from Hosted Checkout

| Feature | Direct API Payment | Hosted Checkout |
|---------|-------------------|-----------------|
| integrate 参数 | `Direct_Payment` | `Hosted_Checkout` |
| 收银台 | 商户自己的收银台 | PayerMax托管收银台 |
| country 参数 | 必填 | 可选 |
| terminalType 参数 | 必填 | 不需要 |
| paymentDetail 参数 | 必填 | 可选 |
| PCI-DSS 要求 | 需要（如自行处理卡号） | 不需要 |

## Notes

- ✓ = Required field
- ✗ = Optional field
- 接口请求成功不代表订单状态成功，需要根据返回的status判断交易状态
- 纯API支付下frontCallbackUrl是必填的，用于支持需要跳转外部的异步交易
