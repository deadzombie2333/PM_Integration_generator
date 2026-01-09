# Tokenization-纯API支付集成

该文档介绍Token支付纯API支付集成模式的集成流程。

**注意**：商户需要具有PCI资质时,才能使用CARD支付方式来集成API模式Token支付。

纯API集成模式下,商户需要自行构建相关的支付页面,如：收银页、支付结果页等,因此,该模式需要商户投入更多的研发成本。

关于纯API集成模式的更多信息,请查看集成模式概览。

## 1. 集成准备

- 注册开发者中心账号；
- 上传测试商户公钥,获取平台公钥、AppID、测试商户号等集成信息；
- 配置回调地址(WebHook),包括支付结果回调地址、退款结果回调地址等；
- 设置测试环境服务器IP白名单；
- 配置并开通相应支付方式；
- 查看不同环境的请求地址；
- 理解请求报文加签和验签的原理,用于生成每次HTTP请求Header的sign签名字符串。

## 2. 交互流程

## 3. 接口列表

| 关联交互时序 | 调用方向 | 接口PATH |
|------------|---------|----------|
| 1.3 创建支付,调用纯API下单 | 商户 -> PayerMax | /orderAndPay |
| 4.1 支付结果异步通知 | PayerMax -> 商户 | /collectResultNotifyUrl |
| 5.1 查询支付交易 | 商户 -> PayerMax | /orderQuery |

## 4. 环境信息

- 测试环境：`https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/<接口PATH>`
- 集成环境：`https://pay-gate.payermax.com/aggregate-pay/api/gateway/<接口PATH>`

## 5. 集成步骤

### 5.1 创建支付

通过调用纯API支付/orderAndPay API 接口,发起HTTP POST请求,创建支付。

**注意**：商户可以通过接口入参expireTime指定单笔支付的支付关单时间,单位是秒,取值须大于1800(30分钟)且小于86400(24小时)。如果传入值小于1800,则系统默认重置为最小值30min；如果传入值小于86400,则系统默认重置为最大值86400。如果商户不指定,则具体的关单时间,根据使用的支付方式会有所不同。

#### 创建支付/orderAndPay API 接口请求示例：

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
        "tokenForFutureUse": true,  // token支付标识
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

#### 无需3ds验证时响应结果：

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "outTradeNo": "test_da78b1f3c2f9443b966347fc89305fc9",
    "tradeToken": "T2024052805951921811176",
    "status": "SUCCESS"
  }
}
```

#### 需要3ds验证时响应结果：

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    // 如果该笔支付会出3ds验证,则会返回3ds验证地址,需要用户完成验证
    "redirectUrl": "https://cashier-n.payermax.com/index.html#/cashier/home?merchantId=020213827212251&merchantAppId=3b242b56a8b64274bcc37dac281120e3&country=ID&tradeToken=TOKEN20220117091121294138752&language=en&token=IHjqkZ8%2F%2FFcnfDPxWTvJFOrulUAKfXFUkxHJSiTdlnjnX1G6AOuTiSl6%2BN05EzxTaJkcSsSyGh5a1q%2FACwWN0sDD%2FgwY5YdWu3ghDcH2wqm%2BJIcEh0qZqo%2BQFnXp65bvkLZnY7VO7HwZGzyrpMBlPhfRCQxwBbc6lJcSYuPf%2Fe8%3D&amount=10000&currency=IDR&frontCallbackUrl=https%3A%2F%2Fwww.payermax.com",
    "outTradeNo": "test_da78b1f3c2f9443b966347fc89305fc9",
    "tradeToken": "T2024052805951921811176",
    "status": "PENDING"
  }
}
```

为了保障用户支付安全,PayerMax或支付渠道可能会发起额外的用户认证流程,常见的有卡支付的3DS支付、钱包支付的用户登录等。如果触发用户认证,则接口响应中会额外返回`redirectUrl`且`data.status=PENDING`,用户可使用`redirectUrl`重定向跳转到相应页面,用户可在该页面完成认证。

### 5.2 跳转用户认证

创建支付/orderAndPay API 接口响应`redirectUrl`表示用户认证页URL,商户接收到响应后,可重定向跳转,用户在该页面完成认证信息填写和提交。

### 5.3 获取支付结果

#### 5.3.1 通过支付结果通知

请查看支付结果-通过支付结果通知。

Token支付通知示例：

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/collectResultNotifyUrl \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
    "appId": "ff4f0273d212386sdxxxxxxxxx",
    "code": "APPLY_SUCCESS",
    "data": {
      "country": "UN",
      "totalAmount": 9.99,
      "channelNo": "PPC8xxxx017516227301xxxx",
      "outTradeNo": "ORDxxxx51006xx",
      "completeTime": "2025-07-04T09:52:11.249Z",
      "currency": "USD",
      "tradeToken": "T20xxx704098xxxx349xx",
      "paymentDetails": [
        {
          "cardInfo": {
            "cardOrg": "VISA",
            "country": "NZ",
            "cardIdentifierNo": "123456******1234",
            "cardIdentifierName": "Z**************"
          },
          "paymentTokenID": "PMTOKEN20230424072005899168200035002",  //只有Token支付会返回该字段
          "paymentMethodType": "CARD"
        }
      ],
      "thirdChannelNo": "151764",
      "status": "SUCCESS"
    },
    "keyVersion": "1",
    "merchantNo": "P01010118640464",
    "msg": "Success.",
    "notifyTime": "2025-07-04T09:52:11.280Z",
    "notifyType": "PAYMENT"
  }'
```

商户响应参数示例：

```json
{
  "msg": "Success",
  "code": "SUCCESS"
}
```

#### 5.3.2 通过支付订单查询

请查看支付结果-通过支付订单查询。

查询入参：

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderQuery \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
    "version": "1.4",
    "keyVersion": "1",
    "requestTime": "2022-01-17T07:51:15.597+00:00",
    "appId": "a0dddd1f622243cb9aa11234e808b5f8",
    "merchantNo": "02021382716699",
    "data": {
      "outTradeNo": "P164241068068119384"  // 商户单号
    }
  }'
```

响应结果：

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "reference": "reference查询和回调返回",
    "country": "SA",
    "totalAmount": 10,
    "outTradeNo": "P164241068068119384",
    "currency": "SAR",
    "channelNo": "DMCP000000000177005",
    "thirdChannelNo": "4ikqJ6ktEqyRawE1dvqb9c",
    "paymentCode": "2312121212",
    "tradeToken": "T2024062702289232000001",
    "completeTime": "2023-10-20T03:28:23.092Z",
    "paymentDetails": [
      {
        "cardInfo": {
          "cardOrg": "VISA",
          "country": "SA",
          "cardIdentifierNo": "400555******0001",
          "cardIdentifierName": "**ngwei"
        },
        "paymentMethodType": "CARD",
        "paymentTokenID": "PMTOKEN20230424072005899168200035002",  //只有Token支付会返回该字段
        "payAmount": 10,
        "exchangeRate": "1",
        "paymentMethod": "CARD",
        "payCurrency": "SAR"
      }
    ],
    "status": "SUCCESS",
    "resultMsg": ""
  }
}
```

### 5.4 使用PaymentTokenID支付

按照上述4步操作,用户完成支付后,PayerMax会将PaymentTokenID返回给商户,商户需要将PaymentTokenID保存起来,并且记录下该paymentTokenID归属于哪个用户、哪个支付方式；

后续支付时,商户使用 /orderAndPay API 将支付方式、用户ID和PaymentTokenID传给PayerMax完成扣款,不再需要上送cardInfo等卡敏感信息。

#### 5.4.1 创建支付

商户通过API模式集成 /orderAndPay API 完成下单支付。

/orderAndPay API 接口请求示例：

```bash
curl --request POST \
  --url 'https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay' \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
    "requestTime": "2025-05-28T03:52:42.591-02:00",
    "keyVersion": "1",
    "appId": "tested7c863c439a9e29b4519867965a",
    "version": "1.4",
    "merchantNo": "TEST10116880289",
    "data": {
      "integrate": "Direct_Payment",  // API模式下,指定Direct_Payment
      "totalAmount": 39.99,
      "country": "SA",
      "expireTime": "3600",
      "paymentDetail": {
        "buyerInfo": {
          "clientIp": "176.16.34.144",
          "userAgent": "Chrome"
        },
        "paymentMethodType": "CARD",
        "paymentTokenID": "PMTOKEN20230424072005899168200035002"
      },
      "frontCallbackUrl": "https://front.your.com/pay/index.html",
      "subject": "River Game HK Limited",
      "outTradeNo": "ov1_da78b1f3c2f9443b966347fc89305fc9",
      "notifyUrl": "https://notify.your.com/pay/paymentWebHookPayerMaxServlet",
      "currency": "SAR",
      "userId": "1822613953000446",
      "terminalType": "WEB"
    }
  }'
```

无需3ds验证时响应结果：

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "outTradeNo": "test_da78b1f3c2f9443b966347fc89305fc9",
    "tradeToken": "T2024052805951921811176",
    "status": "SUCCESS"
  }
}
```

需要3ds验证时响应结果：

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    // 如果该笔支付会出3ds验证,则会返回3ds验证地址,需要用户完成验证
    "redirectUrl": "https://cashier-n.payermax.com/index.html#/cashier/home?merchantId=020213827212251&merchantAppId=3b242b56a8b64274bcc37dac281120e3&country=ID&tradeToken=TOKEN20220117091121294138752&language=en&token=IHjqkZ8%2F%2FFcnfDPxWTvJFOrulUAKfXFUkxHJSiTdlnjnX1G6AOuTiSl6%2BN05EzxTaJkcSsSyGh5a1q%2FACwWN0sDD%2FgwY5YdWu3ghDcH2wqm%2BJIcEh0qZqo%2BQFnXp65bvkLZnY7VO7HwZGzyrpMBlPhfRCQxwBbc6lJcSYuPf%2Fe8%3D&amount=10000&currency=IDR&frontCallbackUrl=https%3A%2F%2Fwww.payermax.com",
    "outTradeNo": "test_da78b1f3c2f9443b966347fc89305fc9",
    "tradeToken": "T2024052805951921811176",
    "status": "PENDING"
  }
}
```

#### 5.4.2 获取支付结果

获取支付结果,可参考第4步中的通过支付结果通知和通过支付订单查询。

## 6. PaymentTokenID管理

商户可通过PaymentTokenID查询 API 接口来查询某用户绑定的所有PaymentTokenID。

当用户想移除绑定的PaymentTokenID时,商户可通过PaymentTokenID解绑 API 来移除PaymentTokenID。

### 6.1 查询PaymentTokenID

商户可以根据支付方式来查询某用户绑定的所有PaymentTokenID,也可指定某个PaymentTokenID来查询,查询结果中会返回对应的掩码卡号和对应PaymentTokenID的状态。

PaymentTokenID查询 API 接口请求示例：

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "{{requestTime}}",
  "appId": "6666c8b036a24579974497c2f9a33333",
  "merchantNo": "010213834784554",
  "data": {
    "userId": "songjiuhuaTest",  // 必填
    "tokenScope": "tokenAcq",  // 必填,固定值tokenAcq
    "paymentMethodType": "CARD",  // 选填
    "targetOrg": null,  // 选填 当paymentMethodType的值不是CARD时,可选填该字段
    "cardOrg": "MASTERCARD",  // 选填,当paymentMethodType的值是CARD时,可选填该字段
    "paymentTokenID": "PMTOKEN20250626075108220812006000001"  // 选填,不填时,会返回该用户绑定的所有paymentTokenID
  }
}
```

PaymentTokenID查询 API 接口响应示例：

```json
{
  "msg": "",
  "code": "APPLY_SUCCESS",
  "data": {
    "tokenList": [
      {
        "tokenScope": "tokenMit",
        "cardInfo": "538774******9957",
        "merchantInitiated": true,
        "paymentTokenStatus": "Activated",
        "userId": "songjiuhuaTest",
        "paymentTokenExpiry": "2099-12-31T23:59:59.000Z",
        "targetOrg": "",
        "ifCVV": "N",
        "paymentTokenID": "PMTOKEN20250523093224475590582000114",
        "accountDisplay": "",
        "paymentMethodType": "CARD",
        "brand": "MASTERCARD"
      },
      {
        "tokenScope": "tokenMit",
        "cardInfo": "538774******1234",
        "merchantInitiated": true,
        "paymentTokenStatus": "Activated",
        "userId": "songjiuhuaTest",
        "paymentTokenExpiry": "2099-12-31T23:59:59.000Z",
        "targetOrg": "",
        "ifCVV": "N",
        "paymentTokenID": "PMTOKEN20250523092615726590582000110",
        "accountDisplay": "",
        "paymentMethodType": "CARD",
        "brand": "MASTERCARD"
      }
    ]
  }
}
```

### 6.2 解绑PaymentTokenID

当用户想移除绑定的PaymentTokenID时,商户可通过该接口来移除PaymentTokenID。移除该PaymentTokenID后,商户将不能再使用该PaymentTokenID来发起支付。

PaymentTokenID解绑 API 接口请求示例：

```json
{
  "version": "1.2",
  "keyVersion": "1",
  "requestTime": "2022-01-22T10:00:00.500+08:00",
  "appId": "46153e2b787241ae8b01857bb087d1bd",
  "merchantNo": "010229810189301",
  "data": {
    "userId": "songjiuhuaTest",
    "paymentTokenID": "PMTOKEN20250523093224475590582000114",
    "removeReason": "user want to remove it"
  }
}
```

PaymentTokenID解绑 API 接口响应示例：

```json
{
  "code": "APPLY_SUCCESS",
  "msg": "Success",
  "data": {
    "paymentTokenID": "PMTOKEN20250523093224475590582000114",
    "userId": "songjiuhuaTest",
    "paymentTokenStatus": "Deleted"
  }
}
```

## 7. 测试上线

在商户完成上述集成步骤后,可以发起实际支付请求进行初步测试验证,具体步骤请查看集成测试-发起测试。

在测试通过后,最终发布上线前,须联系PayerMax技术支持,提交测试的订单信息,以便于PayerMax检查请求日志和数据,确认您已经正确集成相关能力,具体步骤请查看集成测试-发起验收。

验收通过后,商户可以配置生产环境的集成信息,并准备开量事宜。

另外,在收单产品集成下有PayerMax支持的各类支付方式的集成文档,其中包含每种支付方式的测试上线说明。

## 8. 错误排除

测试或验收过程中的响应错误,可以查看错误排查-错误码。

同时,在常见问题中,总结列举各类常见的问题及其处理方式。

您还可以直接联系PayerMax技术支持团队,咨询集成、测试、验收过程中的任何问题。
