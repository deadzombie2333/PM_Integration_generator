# ApplePay周期性订阅集成-PayerMax管理订阅计划

该文档介绍了PayerMax管理周期性订阅计划时，周期性订阅集成ApplePay的相关集成步骤，具体包含：创建订阅计划、激活订阅计划以及接收订阅扣款结果等。

## 1. 前端交互

## 2. 准备事项

根据配置与签名：
- 获取商户自助平台账号
- 获取商户appId和密钥
- 配置异步通知地址
- 配置公钥和私钥

## 3. 创建订阅计划

以下是几种订阅计划类型的API创建请求响应示例，有关完整的API规范，请参阅创建订阅计划 API。

创建订阅计划不同环境的请求地址如下：

**Prod请求地址**：`https://pay-gate.payermax.com/aggregate-pay/api/gateway/subscriptionCreate`

**Test请求地址**：`https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/subscriptionCreate`

### 3.1 普通订阅计划

首期扣款开始时间（firstPeriodStartDate）在请求时间（requestTime）后24小时内，且无优惠配置（trialPeriodConfig）；

创建普通订阅计划入参如下：

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2025-02-26T05:00:00.234+00:00",
  "appId": "6666c8b036a24579974497c2f9a33333",
  "merchantNo": "010213834784554",
  "data": {
    "subscriptionRequestId": "subscription100000000000001", // 必填、商户创建订阅计划的单号
    "userId": "test10001", // 必填、用户id
    "language": "en", // 非必填、 语言
    "callbackUrl": "http://***.com/notifyUrl/subscription",  // 必填、订阅结果和扣款结果的通知地址
    "subscriptionPlan": { // 必填、 订阅计划信息
      "subject": "subject", // 必填、标题
      "description": "PMMAX周期首期扣款", // 非必填、描述
      "totalPeriods": 24, //必填、总期数
      "periodRule": { // 必填、扣款规则
        "periodUnit": "M", // 必填、按月（M），D(日)，W（周），Y（年）扣款
        "periodCount": 2 // 必填、2个月扣款一次
      },
      // 每期扣款金额
      "periodAmount": { //必填
        "amount": 10.0, // 必填
        "currency": "USD" // 必填
      },
      "firstPeriodStartDate": "2025-02-26T12:00:00+00:00", //必填、第一期扣款开始时间传当天，firstPeriodStartDate - requestTime < 24小时
      "advanceDays": 2  // 非必填、指定后续每期的提前扣款天数
    }
  }
}
```

### 3.2 n天试用

首期扣款开始时间（firstPeriodStartDate）在请求时间（requestTime）后，且两个时间相差n天，同时无优惠配置（trialPeriodConfig）。

以下订阅计划入参示例为试用2天的场景，firstPeriodStartDate和requestTime相差2天；

创建2天试用订阅计划入参如下：

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2025-02-26T05:00:00.234+00:00",
  "appId": "6666c8b036a24579974497c2f9a33333",
  "merchantNo": "010213834784554",
  "data": {
    "subscriptionRequestId": "subscription100000000000001", // 必填、商户创建订阅计划的单号
    "userId": "test10001", // 必填、用户id
    "language": "en", // 非必填、 语言
    "callbackUrl": "http://***.com/notifyUrl/subscription",  // 必填、订阅结果和扣款结果的通知地址
    "subscriptionPlan": { // 必填、 订阅计划信息
      "subject": "subject", // 必填、标题
      "description": "PMMAX周期首期扣款", // 非必填、描述
      "totalPeriods": 24, //必填、总期数
      "periodRule": { // 必填、扣款规则
        "periodUnit": "M", // 必填、按月（M），D(日)，W（周），Y（年）扣款
        "periodCount": 2 // 必填、2个月扣款一次
      },
      // 每期扣款金额
      "periodAmount": { //必填
        "amount": 10.0, // 必填、订阅金额
        "currency": "USD" // 必填、订阅币种
      },
      "firstPeriodStartDate": "2025-02-28T05:00:00+00:00", //必填、第一期扣款开始时间传当天，firstPeriodStartDate - requestTime > 24小时
      "advanceDays": 2  // 非必填、指定后续每期的提前扣款天数
    }
  }
}
```

### 3.3 前n期优惠

首期扣款开始时间（firstPeriodStartDate）在请求时间（requestTime）后24小时内，包含优惠配置信息（trialPeriodConfig）。

以下订阅计划入参示例为前2期优惠的场景，优惠期扣款金额为3USD，从第3期开始，扣款金额为10USD；

前2期优惠入参如下：

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2025-02-26T05:00:00.234+00:00",
  "appId": "6666c8b036a24579974497c2f9a33333",
  "merchantNo": "010213834784554",
  "data": {
    "subscriptionRequestId": "subscription100000000000001", // 必填、商户创建订阅计划的单号
    "userId": "test10001", // 必填、用户id
    "language": "en", // 非必填、 语言
    "callbackUrl": "http://***.com/notifyUrl/subscription",  // 必填、订阅结果和扣款结果的通知地址
    "subscriptionPlan": { // 必填、 订阅计划信息
      "subject": "subject", // 必填、标题
      "description": "PMMAX周期首期扣款", // 非必填、描述
      "totalPeriods": 24, //必填、总期数
      "periodRule": { // 必填、扣款规则
        "periodUnit": "M", // 必填、按月（M），D(日)，W（周），Y（年）扣款
        "periodCount": 2 // 必填、2个月扣款一次
      },
      // 每期扣款金额
      "periodAmount": { //必填
        "amount": 10.0, // 必填、订阅金额
        "currency": "USD" // 必填、订阅币种
      },
      "firstPeriodStartDate": "2025-02-28T05:00:00+00:00", //必填、第一期扣款开始时间传当天，firstPeriodStartDate - requestTime > 24小时
      "advanceDays": 2  // 非必填、指定后续每期的提前扣款天数
    }
  }
}
```

创建订阅计划响应参数示例：

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "subscription100000000000001", //创建订阅计划时商户上送的请求单号
    "subscriptionPlan": {
      "subscriptionNo": "SUB20250202620949065212112", // PayerMax生成的订阅单号
      "subscriptionStatus": "INACTIVE" //未激活
    }
  }
}
```

## 4. 激活订阅计划

创建订阅计划后，此时订阅计划处于未激活状态，需用户完成一笔支付或授权来激活订阅计划，订阅计划才能生效。

PayerMax提供了收银台模式、API模式和前置组件模式3种集成模式来完成首笔支付或授权。

### 激活请求参数说明：

- 如果订阅计划类型是n天试用，则激活时totalAmount的值为0；
- 如果订阅计划类型是前n期优惠，则激活时totalAmount的值为优惠期设置的金额；
- 如果订阅计划类型是普通订阅，则激活时totalAmount的值固定期的金额；
- 激活时的currency必须和订阅计划中的币种保持一致；
- 激活时的userId必须和订阅计划中的userId保持一致；
- 激活时必须上送创建订阅计划后PayerMax返回的订阅单号subscriptionNo；
- 激活时subject的值须与订阅计划中的subject保持一致；
- 商户激活订阅计划时，商户需要将订阅计划信息subscriptionPlan传给PayerMax，同时需要上送用户管理订阅计划的地址mitManagementUrl，方便用户访问该地址，可以操作订阅计划，如：取消订阅等；
- API模式激活订阅计划时，商户需要将Apple的支付要素信息上送给PayerMax，否则无法完成订阅计划的激活。

### 4.1 收银台模式激活订阅计划

收银台模式激活订阅计划API文档，请参阅收银台-下单 API。

不同环境的请求地址如下。

**Prod请求地址**：`https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay`

**Test请求地址**：`https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay`

请求参数示例:

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "订阅计划的标题", // 保持和订阅计划的subject一致
    "totalAmount": 10, // 保持和订阅金额一致：【n天试用】时金额为0；【前n期优惠】时金额为优惠期金额；【普通订阅】时金额为每期扣款金额
    "country": "US",
    "currency": "USD", // 保持和订阅币种一致
    "userId": "test1111", // 保持和订阅计划的用户号一致
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Hosted_Checkout", // 激活时为固定值：Hosted_Checkout
    "expireTime": "1800",
    "subscriptionPlan": { // 订阅信息
      "subscriptionNo": "SUB25022603353890000002003" //需要激活的订阅单号
    },
    "mitManagementUrl": "https://[your domain name]/[your subscription management URL]",
    "paymentDetail": {
      "paymentMethodType": "APPLEPAY", //激活时，必传，值为APPLEPAY
      "mitType": "SCHEDULED", // 必传，MIT类型，周期性代扣时为SCHEDULED，非周期性代扣时为UNSCHEDULED
      "tokenForFutureUse": true, // 必传，值为true，生成paymentTokenID，用于后续代扣
      "merchantInitiated": false, // 必传，false标识不是商户主动发起，有用户参与；true标识商户主动发起，不需要用户参与
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
}
```

响应示例:

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    // PayerMax 收银台地址
    "redirectUrl": "https://cashier-n-uat.payermax.com/static/processApiV2.html?tradeToken=T2025042306527802000033&integrate=DIRECT_API&country=UN&payRequestNo=20250423060120EP4366527897000250005&merchantId=010213834784554&merchantAppId=6666c8b036a24579974497c2f9a33333&token=902170aeaadb4621af8d9530398d0efa&orderLan=en&countryLan=en&strategyLan=LUBCO&pmaxLinkV=1",
    "outTradeNo": "APIFOXDEV1745388079422",
    "tradeToken": "T2025042306527802000033",
    "status": "PENDING"
  }
}
```

### 4.2 API模式激活订阅计划

商户需要在商户的收银台上，从Apple钱包中获取Apple的支付要素，调用PayerMax激活订阅计划时，需要将Apple支付要素解密后，上送给PayerMax完成订阅激活。

商户如何自行集成ApplePay请参考：ApplePay-纯API模式集成。

API模式激活订阅计划API文档，请参阅纯API支付 API。

不同环境的请求地址如下：

**Prod请求地址**：`https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay`

**Test请求地址**：`https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay`

请求参数示例:

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "订阅计划的标题", // 保持和订阅计划的subject一致
    "totalAmount": 10, // 保持和订阅金额一致：【n天试用】时金额为0；【前n期优惠】时金额为优惠期金额；【普通订阅】时金额为每期扣款金额
    "country": "US",
    "currency": "USD", // 保持和订阅币种一致
    "userId": "test1111", // 保持和订阅计划的用户号一致
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Direct_Payment", // 激活时为固定值：Direct_Payment
    "expireTime": "1800",
    "subscriptionPlan": { // 订阅信息
      "subscriptionNo": "SUB25022603353890000002003" //需要激活的订阅单号
    },
    "mitManagementUrl": "xxx",
    "terminalType": "WEB", // 终端类型，WEB、WAP or APP
    "osType": "ANDROID", // 操作系统类型 ANDROID or IOS
    "paymentDetail": {
      "paymentMethodType": "APPLEPAY", //必传，值为APPLEPAY
      "mitType": "SCHEDULED", // 必传，MIT类型，周期性订阅时为SCHEDULED，非周期性代扣时为UNSCHEDULED
      "tokenForFutureUse": true, // 必传，值为true，生成paymentTokenID，用于后续代扣
      "merchantInitiated": false, //必传，false表示是需要用户参数；true表示商户发起的代扣，无需用户参与
      "applePayPaymentData": { // 必传，apple支付要素解密后的参数
        "applicationExpirationDate": "231231",
        "applicationPrimaryAccountNumber": "1234209400123456",
        "currencyCode": "344",
        "deviceManufacturerIdentifier": "040010030273",
        "paymentData": {
          "eciIndicator": "7",
          "onlinePaymentCryptogram": "AqhVFUwAAuM69WEZxe+OMAACAAA="
        },
        "paymentDataType": "3DSecure",
        "transactionAmount": "100",
        "network": "Visa",
        "type": "credit",
        "displayName": "VISA 5743"
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
    }
  }
}
```

响应示例:

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422",
    "tradeToken": "T2025042306527802000033",
    "status": "SUCCESS"
  }
}
```

### 4.3 前置组件模式激活订阅计划

前置组件集成请参考：集成步骤。

前置组件模式激活订阅计划时，商户服务端需要调用PayerMax提供的2个API接口：Apply Drop-in Session API 和前置组件支付 API。

#### Apply Drop-in Session接口

不同环境请求地址如下：

**Prod请求地址**：`https://pay-gate.payermax.com/aggregate-pay/api/gateway/applyDropinSession`

**Test请求地址**：`https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/applyDropinSession`

商户客户端集成示例：

```javascript
// 获取 clientKey和sessionKey
const data = await post("applyDropinSession", {
  // 告诉服务端是订阅支付？
  ...params
})

// 创建applepay视图
applePay = PMdropin.create('applepay', {
  clientKey: data.clientKey,
  sessionKey: data.sessionKey,
  theme: yourTheme,
  payButtonStyle: data.yourPayButtonStyle,
  sandbox: data.yourFrameEnv
})

// 挂载dom
applePay.mount('.frame-applepay')

// load 加载事件 判断是否成功加载
applePay.on('load', (res = {}) => {
  const { code, msg } = res || {};
  if(code === "SUCCESS"){
    console.log('[merchant][load]success:', res)
  }else{
    console.log('[merchant][load]fail:', res)
  }
})

// 监听点击applepay按钮的事件，用户选择完订阅计划后，点击applepay按钮的时候可以通过这个事件来监听
applePay.on('payButtonClick', (res) => {
  // 调用PayerMax createSubscription接口创建订阅计划
  createSubscription()
  
  // 禁用applepay按钮点击状态
  applePay.emit('setDisabled', true)
  
  // 需传入subscriptionPlan订阅计划和mitManagementUrl；
  applePay.emit('canMakePayment', { 
    // subscriptionPlan 在周期性订阅的时候必传
    subscriptionPlan: {
      "subject": "subject",
      "description": "PMMAX周期首期扣款。",
      "totalPeriods": 12,
      "periodRule": {
        "periodUnit": "M", // 按月（M），D(日)，W（周），Y（年）扣款
        "periodCount": 1 // // 1个月扣款一次
      },
      "periodAmount": { // 固定期扣款金额
        "amount": 404.35,
        "currency": "SAR"
      },
      "firstPeriodStartDate": "2025-02-26T12:00:00+00:00",
      "trialPeriodConfig": { // 优惠期规则
        "trialPeriodCount": 1, //优惠期数
        "trialPeriodAmount": { // 优惠期扣款金额
          "amount": 10,
          "currency": "SAR"
        }
      }
    },
    mitManagementUrl: "http://www.xxx.com"
  }).then(res => {
    console.log('canMakePayment', res)
    const paymentToken = res?.data?.paymentToken 
    data.paymentToken = paymentToken
    
    // 加密token
    if(paymentToken){
      // 调用PayerMax orderAndPay接口发起支付
      orderAndPay()
    }else{
      // 如果入参不符合格式 这里会抛出错误信息 
      // 错误res示例：{ code: "MIT_PARAMS_VALIDATION_ERROR", message: "xxx  is required" }
      _payLog(JSON.stringify(res))  
      applePay.emit('setDisabled', false)
    }
  }).catch(err => {
    // 如果校验不通过 报明确的错。TODO
    console.log('canMakePayment catch', err)
    applePay.emit('payFail')
    applePay.emit('setDisabled', false)
    _payLog(JSON.stringify(err))      
  })
})
```

Apply Drop-in Session请求入参示例：

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "3b242b56a8b64274bcc37dac281120e3",
  "merchantNo": "020213827212251",
  "data": {
    "totalAmount": "10", // 保持和订阅金额一致：【n天试用】和【n天试用+前n期优惠】时金额为0；【前n期优惠】时金额为优惠期金额；【普通订阅】时金额为每期扣款金额；也可以不填
    "mitType": "SCHEDULED", // 必填，PayerMax管理订阅计划时，值为SCHEDULED
    "currency": "USD", // 必填
    "country": "SA", // 非必填
    "userId": "U10001", // 必填，用户id
    "componentList": [ // 必填，组件支持的支付方式
      "APPLEPAY"
    ]
  }
}
```

响应示例:

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

#### 前置组件支付接口

不同环境的请求地址如下：

**Prod请求地址**：`https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay`

**Test请求地址**：`https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay`

请求参数示例：

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "P1642410680681", // 商户下单唯一单号
    "subject": "订阅计划的标题", // 保持和订阅计划的subject一致
    "totalAmount": 10, // 保持和订阅金额一致：【n天试用】和【n天试用+前n期优惠】时金额为0；【前n期优惠】时金额为优惠期金额；【普通订阅】时金额为每期扣款金额
    "country": "UN",
    "currency": "USD", // 保持和订阅币种一致
    "userId": "test1111", // 保持和订阅计划的用户号一致
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Direct_Payment", // 激活时为固定值：Direct_Payment
    "expireTime": "1800",
    "subscriptionPlan": { // 订阅信息
      "subscriptionNo": "SUB25022603353890000002003" //需要激活的订阅单号
    },
    "mitManagementUrl": "http://www.xxx.com",
    "terminalType": "WEB", // 终端类型，WEB、WAP or APP
    "osType": "ANDROID", // 操作系统类型 ANDROID or IOS
    "paymentDetail": {
      "paymentToken": "CPT4f200d278f3a454b9e91c81edc641e2b", //激活时必传
      "sessionKey": "bdsf8982348974hhf82934bf8239424", //激活时必传
      "mitType": "SCHEDULED", // 必传，MIT类型，周期性代扣时为SCHEDULED，非周期性代扣时为UNSCHEDULED
      "tokenForFutureUse": true, // 必传，值为true，生成paymentTokenID，用于后续代扣
      "merchantInitiated": false, // 必传，false标识不是商户主动发起，有用户参与；true标识商户主动发起，不需要用户参与
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
}
```

响应示例:

```json
{
  "code": "APPLY_SUCCESS",
  "msg": "",
  "data": {
    "outTradeNo": "P1642410680681",
    "tradeToken": "T2024062702289232000001",
    "status": "SUCCESS"
  }
}
```

## 5. 获取订阅计划激活结果

商户可以通过创建订阅计划时上送的callbackUrl地址来接收订阅计划状态变更通知和订阅扣款结果。

### 5.1 获取订阅计划状态变更结果

订阅计划状态变更通知详细通知报文请参考：订阅状态变更通知 API。

订阅激活成功通知参数示例：

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION"
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912",
      "subscriptionStatus": "ACTIVE" // 激活成功
    }
  }
}
```

订阅激活失败通知参数示例：

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION"
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912",
      "subscriptionStatus": "ACTIVE_FAILED" // 激活失败
    }
  }
}
```

商户响应参数示例：

```json
{
  "msg": "Success",
  "code": "SUCCESS"
}
```

### 5.2 获取订阅扣款结果

若创建的订阅计划是普通订阅或前n期优惠，订阅计划激活的同时也会进行首期扣款，扣款完成后，PayerMax会通知商户扣款结果；

订阅扣款结果通知报文请参考：扣款结果通知 API。

扣款成功通知参数示例：

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION_PAYMENT"
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "merchantNo": "P01010113865434",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912"
    },
    "subscriptionPaymentDetail": {
      "subscriptionIndex": 1, // 扣款期数
      "paymentStatus": "SUCCESS", //本期订单状态
      "periodStartTime": "2025-10-13T15:59:59+0000", // 本期开始时间
      "periodEndTime": "2025-12-13T15:59:59+0000", // 本期结束时间
      "payAmount": { // 扣款金额
        "amount": 10,
        "currency": "USD"
      },
      "paymentMethodType": "APPLEPAY",
      "cardOrg": "VISA",
      "lastPaymentInfo": { 
        "tradeToken": "T20221212174800970116912", //支付单号 tradeToken可用于发起退款
        "lastPaymentStatus": "SUCCESS", // 最新扣款结果
        "payTime": "2025-02-13T15:59:59+0000" // 支付时间
      }
    }
  }
}
```

扣款失败通知参数示例：

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION_PAYMENT"
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "merchantNo": "P01010113865434",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912"
    },
    "subscriptionPaymentDetail": {
      "subscriptionIndex": 1, // 扣款期数
      "paymentStatus": "FAILED", //本期订单状态
      "periodStartTime": "2022-10-13T15:59:59+0000", // 本期开始时间
      "periodEndTime": "2022-12-13T15:59:59+0000", // 本期结束时间
      "payAmount": { // 支付金额
        "amount": 10,
        "currency": "USD"
      },
      "paymentMethodType": "APPLEPAY",
      "cardOrg": "VISA",
      "lastPaymentInfo": { 
        "tradeToken": "T20221212174800970116912", //支付单号 tradeToken 可用于退款
        "lastPaymentStatus": "FAILED", // 最新扣款结果
        "payTime": "2022-12-13T15:59:59+0000", // 支付时间
        "errorCode": "xxxx", // 扣款失败code
        "errorMsg": "xxxx" // 扣款失败原因
      }
    }
  }
}
```

商户响应参数示例：

```json
{
  "msg": "Success",
  "code": "SUCCESS"
}
```

### 5.3 获取订阅激活请求结果

商户可以通过激活订阅计划时上送的notifyUrl地址来接收激活请求结果，详细通知报文请参考：支付结果通知 API。

激活请求成功结果示例：

```json
{
  "appId": "d68f5da6a0174388821a64114c6b322c",
  "code": "APPLY_SUCCESS",
  "data": {
    "channelNo": "TPC425300174064927201759000685",
    "completeTime": "2025-02-27T09:41:12.267Z",
    "country": "US",
    "currency": "USD",
    "outTradeNo": "20250227174104451122388",
    "paymentDetails": [
      {
        "applePayInfo": {
          "cardOrg": "VISA",
          "cardIdentifierNo": "123456****1234"
        },
        "paymentMethodType": "APPLEPAY",
        "paymentTokenID": "PMTOKEN20250227071843552050007000094"
      }
    ],
    "reference": "reference",
    "status": "SUCCESS",
    "thirdChannelNo": "mtjxuvedrz58345",
    "totalAmount": 10,
    "tradeToken": "T2025022709425329000091"
  },
  "keyVersion": "1",
  "merchantNo": "P01010118267336",
  "msg": "Success.",
  "notifyTime": "2025-02-27T09:41:12 +0000",
  "notifyType": "PAYMENT"
}
```

激活请求失败结果示例：

```json
{
  "appId": "d68f5da6a0174388821a64114c6b322c",
  "code": "PAYMENT_FAILED",
  "data": {
    "channelNo": "TPC462800174064934688659000687",
    "completeTime": "2025-02-27T09:44:00.216Z",
    "country": "UN",
    "currency": "USD",
    "outTradeNo": "20250227174218727122389",
    "paymentDetails": [
      {
        "applePayInfo": {
          "cardOrg": "VISA",
          "cardIdentifierNo": "123456****1234"
        },
        "paymentMethodType": "APPLEPAY"
      }
    ],
    "reference": "reference",
    "status": "FAILED",
    "thirdChannelNo": "dycbhzfsmz69480",
    "totalAmount": 10,
    "tradeToken": "T2025022709462829000092"
  },
  "keyVersion": "1",
  "merchantNo": "P01010118267336",
  "msg": "Provider failed to process.",
  "notifyTime": "2025-02-27T09:44:00 +0000",
  "notifyType": "PAYMENT"
}
```

商户响应参数示例：

```json
{
  "msg": "Success",
  "code": "SUCCESS"
}
```

## 6. PayerMax后续扣款

订阅计划激活后，PayerMax会按照创建订阅计划时指定的提前扣款天数进行扣款，若未指定提前扣款天数，则会按照PayerMax默认规则进行扣款；

具体扣款规则请参考订阅计划扣款规则说明，如果某期扣款重试后全部失败，PayerMax会将该订阅计划终止，并通知商户；

商户可以通过创建订阅计划时上送的callbackUrl地址来接收扣款结果，详细通知报文请参考：支付结果通知 API。

扣款成功通知参数示例：

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION_PAYMENT"
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "merchantNo": "P01010113865434",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912"
    },
    "subscriptionPaymentDetail": {
      "subscriptionIndex": 1, // 扣款期数
      "paymentStatus": "SUCCESS", //本期订单状态
      "periodStartTime": "2025-10-13T15:59:59+0000", // 本期开始时间
      "periodEndTime": "2025-12-13T15:59:59+0000", // 本期结束时间
      "payAmount": { // 扣款金额
        "amount": 10,
        "currency": "USD"
      },
      "paymentMethodType": "APPLEPAY",
      "cardOrg": "VISA",
      "lastPaymentInfo": { 
        "tradeToken": "T20221212174800970116912", //支付单号 tradeToken可用于发起退款
        "lastPaymentStatus": "SUCCESS", // 最新扣款结果
        "payTime": "2025-02-13T15:59:59+0000" // 支付时间
      }
    }
  }
}
```

扣款失败通知参数示例：

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION_PAYMENT"
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "merchantNo": "P01010113865434",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912"
    },
    "subscriptionPaymentDetail": {
      "subscriptionIndex": 1, // 扣款期数
      "paymentStatus": "FAILED", //本期订单状态
      "periodStartTime": "2022-10-13T15:59:59+0000", // 本期开始时间
      "periodEndTime": "2022-12-13T15:59:59+0000", // 本期结束时间
      "payAmount": { // 支付金额
        "amount": 10,
        "currency": "USD"
      },
      "paymentMethodType": "APPLEPAY",
      "cardOrg": "VISA",
      "lastPaymentInfo": { 
        "tradeToken": "T20221212174800970116912", //支付单号 tradeToken 可用于退款
        "lastPaymentStatus": "FAILED", // 最新扣款结果
        "payTime": "2022-12-13T15:59:59+0000", // 支付时间
        "errorCode": "xxxx", // 扣款失败code
        "errorMsg": "xxxx" // 扣款失败原因
      }
    }
  }
}
```

## 7. 管理订阅计划

订阅计划激活后，可进行订阅计划的管理，如查询订阅扣款结果、取消订阅计划等，订阅计划状态变更后，PayerMax会通知商户订阅计划状态。

### 7.1 订阅状态变更通知

商户可以通过创建订阅计划时上送的callbackUrl地址来接收订阅计划状态变更结果，详细通知报文请参考：订阅状态变更通知 API。

订阅计划终止通知参数示例：

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION"
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912",
      "subscriptionStatus": "TERMINATE"
    }
  }
}
```

### 7.2 取消订阅计划

商户可取消订阅计划，如果正处于最新一期处于扣款中，须等该期扣款成功或扣款失败后，才能取消订阅计划；

详细API报文请参考：取消订阅计划 API。

不同环境的请求地址如下：

**Prod请求地址**：`https://pay-gate.payermax.com/aggregate-pay/api/gateway/subscriptionCancel`

**Test请求地址**：`https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/subscriptionCancel`

取消订阅计划请求参数示例：

```json
{
  "version": "1.5", // 版本为1.5
  "keyVersion": "1",
  "requestTime": "2023-02-13T06:32:50.455+00:00",
  "appId": "82ff47ea6c724a60b666e3ac0ea172dd",
  "merchantNo": "P01010113865434",
  "data": {
    "subscriptionNo": "SUB20221212174716894496912" // PayerMax订阅单号
  }
}
```

取消订阅计划响应参数示例：

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912",
      "subscriptionStatus": "CANCEL" // 已取消
    }
  }
}
```

### 7.3 查询订阅扣款结果

查询订阅扣款结果API文档，请参考：订阅扣款结果查询 API。

不同环境的请求地址如下：

**Prod请求地址**：`https://pay-gate.payermax.com/aggregate-pay/api/gateway/subscriptionQuery`

**Test请求地址**：`https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/subscriptionQuery`

查询订阅计划请求参数示例：

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2023-02-13T06:32:50.455+00:00",
  "appId": "82ff47ea6c724a60b666e3ac0ea172dd",
  "merchantNo": "P01010113865434",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP", //subscriptionNo和requestId必须传一个
    "subscriptionNo": "SUB20221212174716894496912" //subscriptionNo和requestId必须传一个
  }
}
```

查询订阅计划响应参数示例：

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "merchantNo": "P01010113865434",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912",
      "subscriptionStatus": "ACTIVE" // 订阅状态、
    },
    "subscriptionPaymentDetails": [
      {
        "subscriptionIndex": 0, // 扣款期数：第一期
        "paymentStatus": "SUCCESS", //本期订单状态
        "periodStartTime": "2025-01-13T15:59:59+0000", // 本期开始时间
        "periodEndTime": "2025-02-13T15:59:59+0000", // 本期结束时间
        "payAmount": { // 支付金额
          "amount": 100,
          "currency": "SAR"
        },
        "paymentMethodType": "APPLEPAY",
        "cardOrg": "VISA",
        "lastPaymentInfo": { 
          "tradeToken": "T20221212174800970116912", //支付单号 tradeToken 可用于退款
          "lastPaymentStatus": "SUCCESS", // 最新扣款结果
          "payTime": "2025-01-12T15:59:59+0000" // 支付时间
        }
      },
      {
        "subscriptionIndex": 1, // 扣款期数：第二期
        "paymentStatus": "PENDING", //本期订单状态
        "periodStartTime": "2025-02-13T15:59:59+0000", // 本期开始时间
        "periodEndTime": "2025-03-13T15:59:59+0000", // 本期结束时间
        "payAmount": { // 支付金额
          "amount": 100,
          "currency": "SAR"
        },
        "paymentMethodType": "APPLEPAY",
        "cardOrg": "VISA",
        "lastPaymentInfo": { 
          "tradeToken": "T20221212174800970116912", //支付单号 tradeToken 可用于退款
          "lastPaymentStatus": "FAILED", // 最新扣款结果
          "payTime": "2025-02-12T15:59:59+0000", // 支付时间
          "errorCode": "xxxx", // 扣款失败code
          "errorMsg": "xxxx" // 扣款失败原因
        }
      }
    ]
  }
}
```
