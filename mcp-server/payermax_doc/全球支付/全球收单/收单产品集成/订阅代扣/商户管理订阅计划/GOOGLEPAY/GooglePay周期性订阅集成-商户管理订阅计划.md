# GooglePay周期性订阅集成-商户管理订阅计划

该文档介绍了商户管理周期性订阅计划时，周期性订阅集成GooglePay的相关集成步骤，具体包含：绑定支付方式、获取绑定支付方式结果、发起代扣、获取代扣结果等。

## 1. 前端交互

注意：收银台模式下，商户管理订阅计划时，订阅计划详情不会在PayerMax收银台上展示；且由于GooglePay的限制，GooglePay只会对欧洲经济区（European Economic Area，简称"EEA"）展示订阅计划，非EEA地区只展示付款按钮。

## 2. 准备事项

根据配置与签名引导，获取商户自助平台账号、获取商户appId和密钥、配置异步通知地址、配置公钥和私钥。

## 3. 绑定支付方式

核心参数说明：

- **totalAmount**：交易金额，支持传0或者大于0的金额；
- **paymentDetail.mitType**：代扣类型，SCHEDULED标识为周期性订阅，UNSCHEDULED标识为非周期性代扣；
- **paymentDetail.tokenForFutureUse**：true/false，是否需要生成token用于后续代扣；首次绑定支付方式时，该值传true；
- **paymentDetail.merchantInitiated**：true/false，是否是商户发起的交易；首次绑定支付方式时，需要用户参与完成认证或授权，传值为false；
- **mitManagementUrl**：商户管理订阅计划的地址，用户可通过访问该地址操作订阅计划，如取消订阅等；
- **subscriptionPlan**：订阅计划信息。

### 3.1 使用PayerMax收银台绑定支付方式

收银台模式绑定支付方式接口文档，请参阅收银台-下单 API。

不同环境的请求地址如下。

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay

**交易金额大于0元时，请求参数示例:**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "代扣标题", // 标题
    "totalAmount": 10, // 代扣金额
    "country": "US",
    "currency": "USD", // 代扣币种
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Hosted_Checkout", // 固定值：Hosted_Checkout
    "expireTime": "1800",
    "subscriptionPlan": { // 订阅信息
      "subject": "subject",
      "description": "PMMAX周期首期扣款。",
      "totalPeriods": 12,
      "periodRule": {
        "periodUnit": "M", // 按月（M），D(日)，W（周），Y（年）扣款
        "periodCount": 1 // // 1个月扣款一次
      },
      "periodAmount": { // 固定期扣款金额
        "amount": 20,
        "currency": "USD"
      },
      "firstPeriodStartDate": "2025-08-26T12:00:00+00:00",
      "trialPeriodConfig": { // 优惠期规则
        "trialPeriodCount": 1, //优惠期数
        "trialPeriodAmount": { // 优惠期扣款金额
          "amount": 10,
          "currency": "USD"
        }
      }
    },
    "mitManagementUrl": "https://[your domain name]/[your subscription management URL]",
    "paymentDetail": {
      "paymentMethodType": "GOOGLEPAY", //必传，值为GOOGLEPAY
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

**交易金额为0时，请求参数示例:**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "代扣标题", // 标题
    "totalAmount": 0, // 代扣金额
    "currency": "USD", // 代扣币种
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Hosted_Checkout", // 固定值：Hosted_Checkout
    "expireTime": "1800",
    "subscriptionPlan": { //必填 订阅信息
      "subject": "subject",
      "description": "PMMAX周期首期扣款。",
      "totalPeriods": 12,
      "periodRule": {
        "periodUnit": "M", // 按月（M），D(日)，W（周），Y（年）扣款
        "periodCount": 1 // // 1个月扣款一次
      },
      "periodAmount": { // 固定期扣款金额
        "amount": 20,
        "currency": "USD"
      },
      "firstPeriodStartDate": "2025-08-26T12:00:00+00:00",
      "trialPeriodConfig": { // 优惠期规则
        "trialPeriodCount": 1, //优惠期数
        "trialPeriodAmount": { // 优惠期扣款金额
          "amount": 10,
          "currency": "USD"
        }
      }
    },
    "mitManagementUrl": "https://[your domain name]/[your subscription management URL]", //必填
    "paymentDetail": {
      "paymentMethodType": "GOOGLEPAY", //必传，值为GOOGLEPAY
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

**响应示例:**

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

### 3.2 API模式绑定支付方式

商户需要在商户的收银台上，从Google钱包获取支付要素，调用PayerMax绑定支付方式时，需要将Google支付要素解密后，上送给PayerMax完成绑定。

商户如何自行集成GooglePay请参考：GooglePay-纯API模式集成。

API模式绑定支付方式API文档，请参阅纯API支付 API。

不同环境的请求地址如下：

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay

**请求参数示例:**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "代扣标题", // 标题
    "totalAmount": 10, // 代扣金额
    "currency": "USD", // 代扣币种
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Direct_Payment", // 固定值：Direct_Payment
    "expireTime": "1800",
    "terminalType": "WEB", // 终端类型，WEB、WAP or APP
    "osType": "ANDROID", // 操作系统类型 ANDROID or IOS
    "subscriptionPlan": { //非必填 订阅信息
      "subject": "subject",
      "description": "PMMAX周期首期扣款。",
      "totalPeriods": 12,
      "periodRule": {
        "periodUnit": "M", // 按月（M），D(日)，W（周），Y（年）扣款
        "periodCount": 1 // // 1个月扣款一次
      },
      "periodAmount": { // 固定期扣款金额
        "amount": 20,
        "currency": "USD"
      },
      "firstPeriodStartDate": "2025-08-26T12:00:00+00:00",
      "trialPeriodConfig": { // 优惠期规则
        "trialPeriodCount": 1, //优惠期数
        "trialPeriodAmount": { // 优惠期扣款金额
          "amount": 10,
          "currency": "USD"
        }
      }
    },
    "mitManagementUrl": "https://[your domain name]/[your subscription management URL]", //非必填
    "paymentDetail": {
      "paymentMethodType": "GOOGLEPAY", //必传，值为GOOGLEPAY
      "mitType": "SCHEDULED", // 必传，MIT类型，周期性代扣时为SCHEDULED，非周期性代扣时为UNSCHEDULED
      "tokenForFutureUse": true, // 必传，值为true，生成paymentTokenID，用于后续代扣
      "merchantInitiated": false, // false表示是需要用户参数；true表示商户发起的代扣，无需用户参与
      "googlePayDetails": { //必传 google pay下单参数
        "authMethod": "PAN_ONLY", //CRYPTOGRAM_3DS 
        "pan": "4111111111111111", // 卡号
        "expirationMonth": "12",
        "expirationYear": "2029",
        "cryptogram": "xxxxxxxxxxxx",
        "eciIndicator": "5",
        "description": "VISA 1234",
        "cardNetwork": "VISA",
        "cardHolderFullName": "zhangsan" //pan_only传入
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

**响应示例:**

注意：当paymentDetail.googlePayDetails.authMethod=PAN_ONLY时，响应参数redirecUrl将返回3ds验证地址； 当paymentDetail.googlePayDetails.authMethod=CRYPTOGRAM_3DS时，响应参数中不会返回redirecUrl。

```json
//CRYPTOGRAM_3DS响应参数
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

```json
//PAN_ONLY响应参数
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    // 3ds地址
    "redirectUrl": "https://cashier-n.payermax.com/index.html#/cashier/home?merchantId=020213827212251&merchantAppId=3b242b56a8b64274bcc37dac281120e3&country=ID&tradeToken=TOKEN20220117091121294138752&language=en&token=IHjqkZ8%2F%2FFcnfDPxWTvJFOrulUAKfXFUkxHJSiTdlnjnX1G6AOuTiSl6%2BN05EzxTaJkcSsSyGh5a1q%2FACwWN0sDD%2FgwY5YdWu3ghDcH2wqm%2BJIcEh0qZqo%2BQFnXp65bvkLZnY7VO7HwZGzyrpMBlPhfRCQxwBbc6lJcSYuPf%2Fe8%3D&amount=10000¤cy=IDR&frontCallbackUrl=https%3A%2F%2Fwww.payermax.com",
    "outTradeNo": "APIFOXDEV1745388079422",
    "tradeToken": "T2025042306527802000033",
    "status": "SUCCESS"
  }
}
```

### 3.3 使用前置组件绑定支付方式

前置组件绑定支付方式，商户需要通过两个步骤完成集成，具体请参考：集成步骤。

前置组件绑定支付方式时，商户服务端需要调用PayerMax提供的2个API接口：Apply Drop-in Session API 和 前置组件支付 API。

**Apply Drop-in Session接口不同环境请求地址如下：**

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/applyDropinSession
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/applyDropinSession

**商户客户端集成示例：**

```javascript
// 获取 clientKey和sessionKey
const data = await post("applyDropinSession", {
  // 告诉服务端是订阅支付？
  ...params
})

// 创建googlepay视图
googlepay = PMdropin.create('googlepay', {
  clientKey: data.clientKey,
  sessionKey: data.sessionKey,
  theme: yourTheme,
  payButtonStyle: data.yourPayButtonStyle,
  sandbox: data.yourFrameEnv
})

// 挂载dom
googlepay.mount('.frame-googlepay')

// load 加载事件 判断是否成功加载
googlepay.on('load', (res = {}) => {
  const { code, msg } = res || {};
  if(code === "SUCCESS"){
    console.log('[merchant][load]success:', res)
  }else{
    console.log('[merchant][load]fail:', res)
  }
})

// 监听点击googlepay按钮的事件，用户选择完订阅计划后，点击googlepay按钮的时候可以通过这个事件来监听
googlepay.on('payButtonClick', (res) => {
  // 禁用googlepay按钮点击状态
  googlepay.emit('setDisabled', true)
  
  // 需传入subscriptionPlan订阅计划和mitManagementUrl；
  googlepay.emit('canMakePayment', { 
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
      googlepay.emit('setDisabled', false)
    }
  }).catch(err => {
    // 如果校验不通过 报明确的错。TODO
    console.log('canMakePayment catch', err)
    googlepay.emit('payFail')
    googlepay.emit('setDisabled', false)
    _payLog(JSON.stringify(err))      
  })
})
```

**Apply Drop-in Session请求入参示例：**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "3b242b56a8b64274bcc37dac281120e3",
  "merchantNo": "020213827212251",
  "data": {
    "totalAmount": "10", // 代扣金额
    "mitType": "SCHEDULED", // 必填，值为SCHEDULED
    "currency": "USD", // 必填
    "country": "SA", // 非必填
    "userId": "U10001", // 必填，用户id
    "componentList": [ // 必填，组件支持的支付方式
      "GOOGLEPAY"
    ]
  }
}
```

**响应示例:**

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

**前置组件支付接口不同环境的请求地址如下：**

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay

**请求参数示例：**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "代扣标题", // 标题
    "totalAmount": 10, // 代扣金额
    "currency": "USD", // 代扣币种
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test mit",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Direct_Payment", // 固定值：Direct_Payment
    "expireTime": "1800",
    "terminalType": "WEB", // 终端类型，WEB、WAP or APP
    "osType": "ANDROID", // 操作系统类型 ANDROID or IOS
    "subscriptionPlan": { //非必填 订阅信息
      "subject": "subject",
      "description": "PMMAX周期首期扣款。",
      "totalPeriods": 12,
      "periodRule": {
        "periodUnit": "M", // 按月（M），D(日)，W（周），Y（年）扣款
        "periodCount": 1 // // 1个月扣款一次
      },
      "periodAmount": { // 固定期扣款金额
        "amount": 20,
        "currency": "USD"
      },
      "firstPeriodStartDate": "2025-08-26T12:00:00+00:00",
      "trialPeriodConfig": { // 优惠期规则
        "trialPeriodCount": 1, //优惠期数
        "trialPeriodAmount": { // 优惠期扣款金额
          "amount": 10,
          "currency": "USD"
        }
      }
    },
    "mitManagementUrl": "https://[your domain name]/[your subscription management URL]", //非必填
    "paymentDetail": {
      "paymentToken": "CPT4f200d278f3a454b9e91c81edc641e2b", // 必传
      "sessionKey": "bdsf8982348974hhf82934bf8239424", // 必传
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

**响应示例:**

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

## 4. 获取绑定支付方式结果

商户可以通过绑定支付方式时上送的notifyUrl地址来接收绑定支付方式结果，详细结果报文请参考：支付结果通知 API。

**绑定支付方式成功通知参数示例：**

```json
{
  "appId": "d68f5da6a0174388821a64114c6b322c",
  "code": "APPLY_SUCCESS",
  "data": {
    "channelNo": "TPC425300174064927201759000685",
    "completeTime": "2025-02-27T09:41:12.267Z",
    "country": "UN",
    "currency": "USD",
    "outTradeNo": "20250227174104451122388",
    "paymentDetails": [
      {
        "googlePayInfo": {
          "cardIdentifierNo": "123456******1234"
        },
        "paymentMethodType": "GOOGLEPAY",
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

绑定支付方式成功后，PayerMax会生成paymentTokenID，后续代扣时需使用该paymentTokenID来进行代扣。

**绑定支付方式失败通知参数示例：**

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
        "googlePayInfo": {
          "cardIdentifierNo": "123456******1234"
        },
        "paymentMethodType": "GOOGLEPAY",
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

## 5. 发起代扣

参数说明：

- **totalAmount**：交易金额必须大于0；
- **integrate**：传固定值Direct_Payment；
- **paymentDetail.mitType**：代扣类型，SCHEDULED为周期性订阅，UNSCHEDULED为非周期性代扣；
- **paymentDetail.tokenForFutureUse**：true/false，是否需要生成token用于后续代扣；后续扣款，传false或不传；
- **paymentDetail.merchantInitiated**：true/false，是否是商户发起的交易；后续扣款，由商户发起，无需用户参与，传值为true；
- **paymentDetail.paymentTokenID**：绑定方式成功后PayerMax返回的Token。

后续代扣API文档，请参阅纯API支付 API。

不同环境的请求地址如下：

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay

**请求参数示例：**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "代扣标题", // 标题
    "totalAmount": 10, // 代扣金额
    "currency": "USD", // 代扣币种
    "country": "SA", // 必传
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Direct_Payment", // 固定值：Direct_Payment
    "expireTime": "1800",
    "terminalType": "WEB", // 终端类型，WEB、WAP or APP
    "osType": "ANDROID", // 操作系统类型 ANDROID or IOS
    "paymentDetail": {
      "paymentMethodType": "GOOGLEPAY", //必传，值为GOOGLEPAY
      "mitType": "SCHEDULED", // 必传，MIT类型，周期性代扣时为SCHEDULED，非周期性代扣时为UNSCHEDULED
      "tokenForFutureUse": false, // 非必传，值为true，生成paymentTokenID，用于后续代扣
      "merchantInitiated": true, // 必传，false表示是需要用户参数；true表示商户发起的代扣，无需用户参与
      "paymentTokenID": "PMTOKEN20230424072005899168200035002", // 首笔代扣成功后PayerMax返回给商户的Token值
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

**商户响应参数示例：**

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

## 6. 获取代扣结果

无论绑定支付方式还是后续代扣，扣款成功或失败以后，PayerMax会将扣款结果通知给商户，商户也可主动查询代扣结果。

### 6.1 使用callback获取支付结果

商户可以通过支付时上送的notifyUrl地址来接收支付结果，详细通知报文请参考：支付结果通知 API。

**代扣成功通知参数示例：**

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
        "googlePayInfo": {
          "cardIdentifierNo": "123456******1234"
        },
        "paymentMethodType": "GOOGLEPAY",
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

**代扣失败通知参数示例：**

```json
{
  "appId": "d68f5da6a0174388821a64114c6b322c",
  "code": "PAYMENT_FAILED",
  "data": {
    "channelNo": "TPC462800174064934688659000687",
    "completeTime": "2025-02-27T09:44:00.216Z",
    "country": "US",
    "currency": "USD",
    "outTradeNo": "20250227174218727122389",
    "paymentDetails": [
      {
        "googlePayInfo": {
          "cardIdentifierNo": "123456******1234"
        },
        "paymentMethodType": "GOOGLEPAY",
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

接收到通知结果以后，需要响应正确的code和message给PayerMax，否则PayerMax会认为商户未能正常接收到通知消息，会重试通知6次。

**商户响应参数示例：**

```json
{
  "msg": "Success",
  "code": "SUCCESS"
}
```

### 6.2 使用查询获取支付结果

获取支付结果API文档，请参阅交易查询 API。

不同环境的请求地址如下：

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderQuery
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderQuery

**代扣结果查询请求参数示例：**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T07:51:15.597+00:00",
  "appId": "a0dddd1f622243cb9aa1b676e808b5f8",
  "merchantNo": "02021382719993",
  "data": {
    "outTradeNo": "P1642410680681"
  }
}
```

**代扣结果查询响应参数示例：**

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "reference": "reference查询和回调返回",
    "country": "SA",
    "totalAmount": 10,
    "outTradeNo": "P1642410680681",
    "currency": "USD",
    "channelNo": "DMCP000000000177005",
    "thirdChannelNo": "4ikqJ6ktEqyRawE1dvqb9c",
    "paymentCode": "2312121212",
    "tradeToken": "T2024062702289232000001",
    "completeTime": "2023-10-20T03:28:23.092Z",
    "paymentDetails": [
      {
        "targetOrg": "*",
        "googlePayInfo": {
          "cardIdentifierNo": "123456******1234"
        },
        "paymentMethodType": "GOOGLEPAY",
        "paymentTokenID": "PMTOKEN20250224063712195626335000250",
        "payAmount": 10,
        "exchangeRate": "1",
        "payCurrency": "USD"
      }
    ],
    "status": "SUCCESS",
    "resultMsg": ""
  }
}
```

## 7. 解绑支付方式

用户取消代扣后，商户需要为用户解绑该支付方式，解绑支付方式API文档，请参考PaymentTokenID解绑 API。

不同环境的请求地址如下：

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/removePaymentToken
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/removePaymentToken

**请求参数示例：**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-22T10:00:00.500+08:00",
  "appId": "46153e2b787241ae8b01857bb087d1bd",
  "merchantNo": "010229810189301",
  "data": {
    "userId": "TEST",
    "paymentTokenID": "PMTOKEN20230424072005899168200035002",
    "removeReason": "remove"
  }
}
```

**响应参数示例：**

```json
{
  "code": "APPLY_SUCCESS",
  "msg": "Success",
  "data": {
    "paymentTokenID": "PMTOKEN20230424072005899168200035002",
    "userId": "Test",
    "paymentTokenStatus": "Deleted"
  }
}
```
