# Tokenization-前置组件支付集成

该文档介绍Token支付前置组件集成模式的集成流程。

PayerMax通过预先构建的前端UI组件,其可以根据用户选择的不同支付方式,动态展示相应的支付信息输入表单。同时,商户也可以定制化组件的语言、样式等特性。

关于前置组件模式的更多信息,请查看集成模式概览。

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

| 关联交互时序 | 调用方向 | 接口类型 | 接口PATH |
|------------|---------|---------|----------|
| 1.3 获取前置组件初始化信息 | 商户 -> PayerMax | 后端接口 | /applyDropinSession |
| 1.6 创建并挂载PayerMax组件 | 商户客户端 -> PayerMax前置组件JS SDK | 前端接口 | PMdropin.create |
| 1.6 创建并挂载PayerMax组件 | 商户客户端 -> PayerMax前置组件JS SDK | 前端接口 | PMdropin.mount |
| 1.6 创建并挂载PayerMax组件 | 商户客户端 -> PayerMax前置组件JS SDK | 前端接口 | PMdropin.on |
| 2.2 获取paymentToken | 商户客户端 -> PayerMax前置组件JS SDK | 前端接口 | PMdropin.emit |
| 3.4 创建支付,调用前置组件下单接口 | 商户 -> PayerMax | 后端接口 | /orderAndPay |
| 4.1 支付结果异步通知 | PayerMax -> 商户 | 后端接口 | /collectResultNotifyUrl |
| 5.1 查询支付交易 | 商户 -> PayerMax | 后端接口 | /orderQuery |

## 4. 环境信息

- 测试环境：`https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/<接口PATH>`
- 集成环境：`https://pay-gate.payermax.com/aggregate-pay/api/gateway/<接口PATH>`

## 5. 集成步骤

### 5.1 获取前置组件初始化信息

商户服务端通过/applyDropinSession API 接口,发起HTTP POST请求,获取前置组件初始化所需的客户端令牌clientKey和会话令牌sessionKey。

#### /applyDropinSession API 接口请求示例：

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/applyDropinSession \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
    "version": "1.4",
    "keyVersion": "1",
    "requestTime": "2025-05-14T16:30:27.174+08:00",
    "appId": "test516e8ab74578be8eecd8c4803fbe",
    "merchantNo": "TEST010117960578",
    "data": {
      "country": "MY",  // 收单国家
      "currency": "MYR",  // 订单币种
      "totalAmount":"50",  // 订单金额
      "tokenForFutureUse": true,  // 传true,则表示该笔请求Token支付请求,组件上会显示Token协议
      "userId": "20220622_00086",  // 用户ID,须保持唯一
      "componentList":["CARD"]  // 指定本次订单支付可用的支付方式
    }
  }'
```

可以通过请求参数`componentList`指定本次订单实际可用的支付方式,取值必须是商户已经签约的支付方式。商户可通过商户平台(MMC)查询已签约的支付方式,或者咨询PayerMax技术支持。

#### /applyDropinSession API 接口响应示例：

```json
{
  "msg": "success",
  "code": "APPLY_SUCCESS",
  "data": {
    "sessionKey": "bf2c47b085e24c299e45dd56fd751a70",
    "clientKey": "bbd8d2639a7c4dfd8df7d005294390df"
  }
}
```

### 5.2 渲染前置组件

在相关 HTML 页面上引入 CDN 包。

```html
<script src="https://cdn.payermax.com/dropin/js/pmdropin.min.js"></script>
```

通过div标签,在商户页面嵌入一个iframes。

```html
<div class="frame-card">
  <!-- 表单内容 -->
</div>
```

初始化 PayerMax Frames。

```javascript
// 初始化卡组件,可参考https://docs.payermax.com/doc-center/receipt/front-end-component/configuration-card.html
const card = PMdropin.create('card', {
  clientKey: "客户端公钥",  // 在步骤1.1中获取到的 data.clientKey
  sessionKey: "会话令牌",  // 在步骤1.1中获取到的 data.sessionKey
  sandbox: false,  // 默认是 false,即生产环境
  hideSaveCard: false,  //是否隐藏保存卡信息选项,默认是false展示
  hideCardBrands: false,  //是否隐藏左上角卡品牌的Logo,默认是false展示
  hideRecommendAccount: true  // 是否在组件上隐藏推荐卡,默认是false展示
});

// 挂载实例
card.mount('.frame-card');  // 将挂载至匹配到的第一个dom元素上

// 组件加载完成时机
card.on('ready', () => {
  // 移除自定义loading               
})
```

监听表单填写状态,动态设置支付按钮(可选)。

通过表单监听事件,可实时监控用户填写信息的合法性,以此动态设定 支付 按钮是否可点击。

```javascript
card.on('form-check', (res) => {
  // res.isFormValid 为表单状态。取值是false/true
  // true 表示表单校验通过,可支付；false 表示校验未通过,不可支付,无法点击支付按钮。
  console.log('[dropin][form-check]:', res)
})
```

#### 勾选token支付协议

不勾选Token支付协议,会走到普通支付流程,支付完成后,不会返回商户PaymentTokenID；只有用户勾选Token协议后,支付完成后,才会返回商户PaymentTokenID。

下载完整的前端组件集成DEMO示例,替换sessionKey和clientKey后,可本地运行并查看前置组件集成样例。

### 5.3 创建支付

商户客户端：用户点击发起支付,检查是否可支付,并获取paymentToken。

```javascript
card.emit('setDisabled', true)  // 点击支付按钮后冻结表单,防止重复提交支付过程
card.emit('canMakePayment').then(res => {
  if (res.code === 'APPLY_SUCCESS') {
    const paymentToken = res.data.paymentToken  // 支付token,支付接口使用
    // 发起支付接口
    // 商户自己请求后端接口进行下单,
    // 商户自己用params构造请求参数,需要带上paymentToken。
    // res.data.agreementAccepted = true,表示用户勾选了token协议,
    // res.data.agreementAccepted = false,表示用户未勾选了token协议,
    // 只有res.data.agreementAccepted=true时,商户在调用orderAndPay接口时
    // 才能上送data.paymentDetail.tokenForFutureUse=true,否则下单会失败
    _postapi('orderAndPay',params).then(res =>{
      const code = (res || {}).code
      //商户将支付结果返回到前端
      if (code == 'APPLY_SUCCESS') {
        //支付成功,展示支付结果
      } else {
        //支付失败,展示支付结果
      }
    }
    card.emit('setDisabled', false)  // 支付接口完成后解冻表单
  }
}).catch(err => {
  card.emit('setDisabled', false)  // 发生异常后解冻表单
})
```

`canMakePayment`返回结果如下：

```json
{
  "code": "APPLY_SUCCESS",
  "message": "",
  "data": {
    "paymentToken": "xxxxxxx",
    "cardBinNo": "123456",
    "maskCardNumber": "123456****1234",
    "cardHolderFullName": "zhangsan",
    "cardOrg": "VISA",
    "cardType": "CREDIT",
    "cardIssuingCountry": "SA",
    "cardExpirationMonth": "12",
    "cardExpirationYear": "33",
    "agreementAccepted": true  // true标识商户同意token协议
  }
}
```

商户服务端：调用/orderAndPay API 接口发起HTTP POST请求,创建支付。

**注意**：创建支付后,商户可以通过接口入参expireTime指定单笔支付的支付关单时间,单位是秒,取值须大于1800(30分钟)且小于86400(24小时)。如果传入值小于1800,则系统默认重置为最小值30min；如果传入值小于86400,则系统默认重置为最大值86400。如果商户不指定,则具体的关单时间,根据使用的支付方式会有所不同。

#### /orderAndPay API 接口请求示例：

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
      "integrate": "Direct_Payment",  // 前置组件模式下,指定Direct_Payment
      "totalAmount": 39.99,
      "country": "SA",
      "expireTime": "3600",
      "paymentDetail": {
        // 支付时,通过JS SDK的emit接口的canMakePayment事件响应获取,非空
        "paymentToken": "TEST12637c2c2d942239d9a2661c4ad14f9",
        "buyerInfo": {
          "clientIp": "176.16.34.144",
          "userAgent": "Chrome"
        },
        // 支付时,通过JS SDK的create接口的响应获取,非空
        "sessionKey": "test29632c3643768e3b65ef6a31c9ce",  // 前置组件模式下非空
        "tokenForFutureUse": true  // tokenForFutureUse传ture需要满足2个条件：
        // 1、apply Paymentession入参需要指定tokenForFutureUse=true
        // 2、用户需在组件上勾选了token协议
        // 如果未满足上面2个条件,但是该接口传了tokenForFutureUse=true,则下单会校验失败
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

#### /orderAndPay API 接口响应示例：

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

### 5.4 获取支付结果

Token支付的订单,支付完成以后,会在结果通知中返回paymentTokenID,商户获取到paymentTokenID后,需要保存起来,并且记录下该paymentTokenID归属于哪个用户、哪个支付方式；方便后续支付使用paymentTokenID替代支付要素(卡号等信息)完成支付。

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
