# Tokenization-收银台支付集成

该文档介绍Token支付收银台集成模式的集成流程。

收银台集成模式下,用户下单后,跳转到PayerMax构建的H5收银页面支付。PayerMax H5收银页面展示可选的支付方式列表,同时支持自适应设备屏幕大小、多语言等特性。

该集成模式下,商户无需开发收银台页面,可极大简化商户集成,缩短上线周期。

关于收银台集成模式的更多信息,请查看集成模式概览。

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
| 1.3 创建支付,调用收银台下单接口 | 商户 -> PayerMax | /orderAndPay |
| 5.1 支付结果异步通知 | PayerMax -> 商户 | /collectResultNotifyUrl |
| 6.1 查询支付交易 | 商户 -> PayerMax | /orderQuery |

## 4. 环境信息

- 测试环境：`https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/<接口PATH>`
- 集成环境：`https://pay-gate.payermax.com/aggregate-pay/api/gateway/<接口PATH>`

## 5. 集成步骤

### 5.1 创建支付

收银台模式Token支付场景,目前不支持全量收银台,只支持指定支付方式或指定支付方式+目标机构。

通过调用创建支付/orderAndPay API 接口,发起HTTP POST请求,创建支付。

PayerMax收银台集成模式下,支持商户自定义供用户选择的可用支付方式。如果商户不指定支付方式,默认展示全量支付方式,用户交互界面展示请查看收银台模式介绍；如果商户指定支付方式,PayerMax收银页会根据请求入参设定,选择性展示部分可用支付方式。

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
    "keyVersion": 1,
    "requestTime": "2025-05-14T16:30:27.174+08:00",
    "appId": "test516e8ab74578be8eecd8c4803fbe",
    "merchantNo": "TEST010117960578",
    "data": {
      "outTradeNo": "test5141630270627",
      "integrate": "Hosted_Checkout",
      "subject": "US $4.99 Stargem",
      "totalAmount": 4.99,
      "currency": "USD",
      "country": "US",
      "frontCallbackUrl": "https://pay.your.com/official_v2/redirect/web_payermax_web_v1",
      "userId": "test_1743900006925",
      "reference": "gp_huq_u",
      "notifyUrl": "https://pay.your.com/official_v2/notify/web_payermax_web_v1",
      "paymentDetail": {
        "paymentMethodType": "CARD",  // 指定支付方式
        "allowedCardOrg": [  // 指定卡组,可以为空
          "MASTERCARD"
        ],
        "tokenForFutureUse": true,
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
      }
    }
  }'
```

如果商户希望限定用户支付的卡品牌,可以通过设定请求入参`paymentDetail.allowedCardOrg`实现。如上例中,指定卡品牌为万事达,则当PayerMax渲染收银页时,只会展示支持万事达的支付机构。

#### 创建支付/orderAndPay API 接口响应示例：

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "redirectUrl": "https://cashier-n.payermax.com/v2/index.html#/payments?merchantId=TEST010117960578&merchantAppId=test516e8ab74578be8eecd8c4803fbe&orderNo=test5141630270627&country=US&tradeToken=T2019051408217377899667&paymentMode=CARD&targetOrg=*&token=acd8b556379140ee9a6ea067d6e68e35&amount=4.99&currency=USD&version=1.4&cashierId=T2019051408217377899667&frontCallbackUrl=https%3A%2F%2Fpay.your.com%2Fofficial_v2%2Fredirect%2Fweb_payermax_web_v1&pmaxLinkV=1",
    "outTradeNo": "test5141630270627",  // 商户交易单号,与请求中outTradeNo一致
    "tradeToken": "T2019051408217377899667",  // PayerMax交易单号
    "status": "PENDING"
  }
}
```

### 5.2 跳转PayerMax收银页

创建支付/orderAndPay API 接口响应`redirectUrl`表示PayerMax收银页URL,商户接收到响应后,可重定向跳转PayerMax收银页,用户在该页面完成支付。

### 5.3 跳转支付结果页

用户完成支付后,PayerMax收银页会重定向跳转至PayerMax支付结果页。

PayerMax支付结果页会展示支付结果(如下图所示),页面中包含 关闭 或 返回 按钮,用户点击后,跳转到商户指定的页面`frontCallBackUrl`。

商户应该保证自己传入的`frontCallBackUrl`在外部浏览器上可用。

不同`frontCallBackUrl`形式的跳转差异如下：

| frontCallBackUrl形式 | 支付完成后跳转流程 | 是否推荐 | 优点 | 缺点 |
|---------------------|------------------|---------|------|------|
| 普通h5 (http/https) | 停留在系统浏览器,展示该H5页面 | 否 | / | 不具备唤起APP能力 |
| 内置主动唤起 APP逻辑h5 (http/https) | 展示该H5页面,同时由页面内逻辑主动识别场景进行商户APP唤起操作,或停留在本页面 | 是 | 逻辑灵活、流程可控 | 开发复杂,要唤起APP仍需搭配 URL Scheme 或 AppLink/Universal Link 使用 |
| URL Scheme (自定义scheme://) | 展系统自动尝试唤起Scheme指定APP。若APP存在且具备权限,可打开对应APP；若APP不存在或无权限,停留在系统浏览器,展示空白页 | 否 | 简单易开发 | 无降级逻辑,未唤起 APP 时将展示空白页 |
| AppLink/Universal Link (http/https) | 系统自动尝试唤起Scheme指定APP。若APP存在且具备权限,可打开对应APP；若APP不存在或无权限,停留在系统浏览器,展示降级H5页面内容 | 是 | 开发逻辑相对简单、可降级使用H5处理业务逻辑 | |

返回商户的URL由两部分组成,第一部分是创建支付/orderAndPay API 接口请求的`frontCallbackUrl`,第二部分是PayerMax附加的额外参数。

如下是一个完整的跳转URL示例：

其中PayerMax附加的额外参数包括：

- `outTradeNo`：商户订单号；
- `tradeToken`：PayerMax订单号；
- `status`：订单状态。

**特别注意**：请勿直接使用该值更新商户订单状态,应按照步骤4：获取支付结果,作为处理依据,以此确保交易状态的准确性。

### 5.4 获取支付结果

#### 5.4.1 通过支付结果通知

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

#### 5.4.2 通过支付订单查询

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

### 5.5 使用PaymentTokenID支付

按照上述4步操作,用户完成支付后,PayerMax会将PaymentTokenID返回给商户,商户需要将PaymentTokenID保存起来,并且记录下该paymentTokenID归属于哪个用户、哪个支付方式；

后续支付时,商户使用 /orderAndPay API 将支付方式、用户ID和PaymentTokenID传给PayerMax完成扣款,不再需要上送cardInfo等卡敏感信息。

#### 5.5.1 创建支付

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

#### 5.5.2 获取支付结果

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
