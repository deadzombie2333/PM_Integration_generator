# Apply Drop-in Session

## 接口信息

**请求方式:** POST

**请求地址:** `https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/applyDropinSession`

**接口说明:** 在商户服务端调用该接口,获取用于初始化前置组件的主要参数

## Request

### Headers

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| Content-Type | string | 是 | 内容类型 | application/json |
| sign | string | 是 | 签名信息,请参考技术文档 | FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A== |

### Body (application/json)

| 参数名 | 类型 | 必填 | 说明 | 限制 |
|--------|------|------|------|------|
| version | string | 是 | 接口版本,当前值为:1.6 | <= 8 characters |
| keyVersion | string | 是 | 密钥版本,当前值为:1 | <= 8 characters |
| requestTime | string | 是 | 请求时间,符合rfc3339规范,格式:yyyy-MM-dd'T'HH:mm:ss.SSSXXX 时间需要在当前时间两分钟内 | <= 32 characters |
| appId | string | 是 | 商户应用Id,PayerMax分配给商户应用的唯一标识 | <= 64 characters |
| merchantNo | string | 否 | 商户号,商户与PayerMax业务签约时生成的唯一标识 | <= 32 characters |
| data | object | 是 | 请求数据体 | - |

#### data 对象

| 参数名 | 类型 | 必填 | 说明 | 限制 |
|--------|------|------|------|------|
| totalAmount | string | 否 | 非必填,如果需要传值,则只有传了mitType时,totalAmount才支持传0;其他情况需要大于0 | - |
| mitType | string | 否 | 签约代扣产品后,可传mitType | 可选值:SCHEDULED, UNSCHDULED |
| captureMode | string | 否 | 请款模式 | MANUAL |
| authorizationType | string | 否 | 授权类型 | FINAL_AUTH |
| currency | string | 是 | 标价币种,大写字母,参见【交易支持国家/地区与币种】 | <= 3 characters |
| country | string | 是 | 国家代码,大写字母,参见【交易支持国家/地区与币种】。如指定了paymentMethodType,则国家代码必须上送且和支付方式对应国家匹配。收银台可用国家地区选择策略为:上送国家代码地区>用户历史使用国家代码地区>用户IP所在国家代码地区。(可用国家地区:交易币种对应的国家与签约国家取交集) | <= 2 characters |
| userId | string | 是 | 商户内部的用户Id,需要保证每个ID唯一性。支付方式绑定后会根据userId进行支付方式推荐 | <= 64 characters |
| referralCode | string | 否 | 用于更精准的支付方式推荐,如设备ID、设备指纹等 | <= 32 characters |
| componentList | array[string] | 否 | 组件列表 | 可选值:CARD, APPLEPAY |

## Response

### 200 成功响应

#### Body (application/json)

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | string | 是 | 响应码 |
| msg | string | 是 | 响应消息 |
| data | object | 是 | 返回数据体 |

#### data 对象

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| sessionKey | string | 是 | Drop-in会话密钥 |
| clientKey | string | 是 | 前端SDK初始化参数 |
