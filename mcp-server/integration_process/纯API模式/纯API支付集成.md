# 纯API支付集成

## 概述

该文档介绍纯API支付集成模式的集成流程。纯API集成模式下，商户需要自行构建相关的支付页面，如：收银页、支付结果页等，因此，该模式需要商户投入更多的研发成本。

关于纯API集成模式的更多信息，请查看集成模式概览。

## 1. 集成准备

- 注册开发者中心账号
- 上传测试商户公钥，获取平台公钥、AppID、测试商户号等集成信息
- 配置回调地址（WebHook），包括支付结果回调地址、退款结果回调地址等
- 设置测试环境服务器IP白名单
- 配置并开通相应支付方式
- 查看不同环境的请求地址
- 理解请求报文加签和验签的原理，用于生成每次HTTP请求Header的sign签名字符串

## 2. 交互流程

```
用户 -> 商户收银页 -> 商户后端 -> PayerMax -> 用户认证(如需要) -> 支付完成 -> 结果通知 -> 商户
```

## 3. 接口列表

| 关联交互时序 | 调用方向 | 接口PATH |
|------------|---------|----------|
| 1.3 创建支付，调用纯API下单 | 商户 -> PayerMax | /orderAndPay |
| 4.1 支付结果异步通知 | PayerMax -> 商户 | /collectResultNotifyUrl |
| 5.1 查询支付交易 | 商户 -> PayerMax | /orderQuery |

## 4. 环境信息

- **测试环境**: `https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/<接口PATH>`
- **集成环境**: `https://pay-gate.payermax.com/aggregate-pay/api/gateway/<接口PATH>`

## 5. 集成步骤

### 5.1 创建支付

通过调用纯API支付 `/orderAndPay` API 接口，发起HTTP POST请求，创建支付。

**注意**：
- 商户可以通过接口入参 `expireTime` 指定单笔支付的支付关单时间，单位是秒
- 取值须大于1800（30分钟）且小于86400（24小时）
- 如果传入值小于1800，则系统默认重置为最小值30min
- 如果传入值大于86400，则系统默认重置为最大值86400
- 如果商户不指定，则具体的关单时间根据使用的支付方式会有所不同

#### 创建支付请求示例

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
    "version": "1.4",
    "keyVersion": "1",
    "requestTime": "2025-05-21T07:56:20.657+00:00",
    "appId": "test81af1bdd45c4be5318305e279061",
    "merchantNo": "TEST20118706753",
    "data": {
      "outTradeNo": "test598684645",
      "subject": "Women'\''s Long Skirts",
      "integrate": "Direct_Payment",
      "totalAmount": "74.99",
      "currency": "USD",
      "country": "AU",
      "userId": "84645",
      "language": "en",
      "reference": "2476598332645",
      "frontCallbackURL": "https://your.com/checkout-2/order-received/84645",
      "notifyUrl": "https://your.com/?wc-api=wc_payermaxcallback",
      "terminalType": "WEB",
      "paymentDetail": {
        "paymentMethodType": "CARD",
        "cardInfo": {
          "cardIdentifierNo": "455803****0807",
          "cardHolderFullName": "test holder",
          "cardExpirationMonth": "08",
          "cardExpirationYear": "19",
          "cvv": "808"
        },
        "buyerInfo": {
          "firstName": "Deborah",
          "lastName": "Swinstead",
          "email": "your@gmail.com",
          "phoneNo": "0609 031 114",
          "address": "Test Address",
          "city": "Holden Hill",
          "region": "SA",
          "zipCode": "5088",
          "clientIp": "211.52.321.225",
          "userAgent": "Mozilla/5.0 (iPad; CPU OS 18_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/22E252 [FBAN/FBIOS;FBAV/513.1.0.55.90;FBBV/735017191;FBDV/iPad13,16;FBMD/iPad;FBSN/iPadOS;FBSV/18.4.1;FBSS/2;FBID/tablet;FBLC/en_GB;FBOP/5;FBRV/737247184]"
        }
      },
      "goodsDetails": [
        {
          "goodsId": "49373",
          "goodsName": "Women'\''s Long Skirts",
          "quantity": "2",
          "price": "38",
          "goodsCategory": "skirt",
          "showUrl": "https://your.com/product/womens-floral-print-elastic-high-waist-pleated-ruffle-flowy-long-skirts/"
        }
      ],
      "shippingInfo": {
        "firstName": "test",
        "lastName": "test",
        "email": "test@gmail.com",
        "phoneNo": "0609 031 114",
        "address1": "Test Address",
        "address2": "un",
        "address3": "Test Address, SA 5088",
        "city": "Holden Hill",
        "region": "SA",
        "state": "SA",
        "country": "AU",
        "zipCode": "5088"
      },
      "billingInfo": {
        "firstName": "test",
        "lastName": "test",
        "email": "test@gmail.com",
        "phoneNo": "0609 031 114",
        "address1": "Test Address",
        "address2": "un",
        "address3": "Test Address, SA 5088",
        "city": "Holden Hill",
        "region": "SA",
        "state": "SA",
        "country": "AU",
        "zipCode": "5088"
      },
      "envInfo": {
        "deviceLanguage": "en-AU",
        "screenHeight": "1180",
        "screenWidth": "820"
      }
    }
  }'
```

#### 创建支付响应示例（直接成功）

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "outTradeNo": "test598684645",
    "tradeToken": "T20290323107917693601854",
    "status": "SUCCESS"
  }
}
```

#### 创建支付响应示例（需要用户认证）

为了保障用户支付安全，PayerMax或支付渠道可能会发起额外的用户认证流程，常见的有：
- 卡支付的3DS认证
- 钱包支付的用户登录

如果触发用户认证，则接口响应中会额外返回 `redirectUrl` 且 `data.status=PENDING`。

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "outTradeNo": "test598684645",
    "tradeToken": "T20290323107917693601854",
    "status": "PENDING",
    "redirectUrl": "https://3ds-auth.payermax.com/verify?token=xxx"
  }
}
```

### 5.2 跳转用户认证

创建支付 `/orderAndPay` API 接口响应 `redirectUrl` 表示用户认证页URL，商户接收到响应后，可重定向跳转，用户在该页面完成认证信息填写和提交。

**常见认证场景**：

#### 3DS认证（卡支付）
- 用户需要输入银行发送的验证码
- 或完成银行APP内的认证
- 认证完成后自动返回

#### 钱包登录认证
- 用户需要登录钱包账户
- 确认支付信息
- 完成支付操作

### 5.3 获取支付结果

#### 5.3.1 通过支付结果通知

请查看支付结果-通过支付结果通知。

#### 5.3.2 通过支付订单查询

请查看支付结果-通过支付订单查询。

## 6. 测试上线

在商户完成上述集成步骤后，可以发起实际支付请求进行初步测试验证，具体步骤请查看集成测试-发起测试。

在测试通过后，最终发布上线前，须联系PayerMax技术支持，提交测试的订单信息，以便于PayerMax检查请求日志和数据，确认您已经正确集成相关能力，具体步骤请查看集成测试-发起验收。

验收通过后，商户可以配置生产环境的集成信息，并准备开量事宜。

另外，在收单产品集成下有PayerMax支持的各类支付方式的集成文档，其中包含每种支付方式的测试上线说明。

## 7. 错误排除

测试或验收过程中的响应错误，可以查看错误排查-错误码。

同时，在常见问题中，总结列举各类常见的问题及其处理方式。

您还可以直接联系PayerMax技术支持团队，咨询集成、测试、验收过程中的任何问题。
