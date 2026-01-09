# ApplePay-纯API模式集成

该文档介绍纯API模式下，使用ApplePay的集成步骤。

纯API集成模式下，商户需要自行构建相关的支付页面，如：收银页、支付结果页等；此外，还需要商户进行复杂的证书配置以及加解密处理。因此，该模式需要商户投入更多的研发成本。

关于纯API集成模式的更多信息，请查看集成模式概览。

## 1. 交互流程

商户需要自己获取ApplePay Token，解密Token得到卡信息，然后将解密后的卡信息传递给PayerMax。

## 2. 集成准备

根据配置与签名引导，获取PayerMax侧的：
- 商户自助平台账号
- 商户appId和密钥
- 配置异步通知地址
- 配置公钥和私钥

进行ApplePay的相关证书配置流程，主要包括：
1. 创建商户IDs
2. 注册并验证商户域名
3. 创建 Payment Processing Certificate
4. 创建 Merchant Identity Certificate

> **注意**: 若商户已完成ApplePay的相关证书配置流程，可直接按照步骤3.4进行对接即可。

### 2.1 创建商户IDs

1. 登录 [Apple Developer](https://developer.apple.com/)，添加 Merchant ID
2. 进入对应模块：**Certificates, Identifiers & Profiles** → **Identifiers** → **Merchant IDs**

### 2.2 注册并验证商户域名

#### 域名要求

- 使用ApplePay的页面必须使用 **HTTPS** 访问
- 该页面的域名必须有SSL证书
- ApplePay会在处理过程中验证该域名证书的有效性，证书过期则无法提供服务
- 域名不能位于代理服务器或者重定向后，并且允许Apple服务器访问
- 详情请参考：[Allow Apple IP Addresses for Domain Verification](https://developer.apple.com/documentation/apple_pay_on_the_web/setting_up_your_server#3172427)

一个Merchant ID下可以添加多个域名。

#### 验证步骤

1. 添加域名后下载域名验证文件
2. 将下载到的域名验证文件上传到自己服务上
3. 确保可以通过以下URL访问到该文件：
   ```
   https://yourdomain.com/.well-known/apple-developer-merchantid-domain-association.txt
   ```
   - 使用自己的真实域名替换 `yourdomain.com`
   - 在你的Web服务器根目录下创建一个文件夹 `.well-known` 并将下载到的文件放在该文件夹中

4. 配置好域名验证文件后在Apple Developer后台进行域名有效性验证
5. 验证通过后操作界面会展示验证有效期，该有效期等同于域名SSL证书的有效期

> **注意**: 示例图片中时间差异是因为两者采用了不同的时区展示。

#### 证书过期更新

> **特别提醒**: Apple 会在域名SSL证书过期前的30天、15天、7天分别去检查你的域名证书是否更新。

- 如果你在证书过期前完成了更新，Apple检测到了更新后的证书并且域名验证没问题，那么你不需要做任何额外的事情
- 如果没有在证书过期前完成更新，则要重新下载域名认证文件并再次完成验证（参考第2、3步）
- **最佳实践**: 在域名证书过期前的7天之前完成证书更新，这样在7天的检查中可以拿到更新后的证书信息

### 2.3 创建 Payment Processing Certificate

该证书用于Server端和ApplePay的交互，属于正常HTTPS请求的客户端证书。

操作步骤请参考 [Apple官方文档](https://developer.apple.com/documentation/apple_pay_on_the_web/configuring_your_environment)。

#### 2.3.1 生成 Certificate Signing Request (CSR)

两种方式：
1. 参考Apple官方文档，使用Keychain Access生成
2. 使用命令行生成（推荐）

**使用命令行生成：**

1. 需要先安装OpenSSL
2. 生成私钥，需使用ECC算法，256长度：
   ```bash
   openssl ecparam -genkey -name prime256v1 -out applepay-ppc-ecc-256-private.key
   ```
   会得到 `applepay-ppc-ecc-256-private.key` 文件，这个就是私钥，需要保存到系统中，后续解密Token会用到。

3. 生成csr文件：
   ```bash
   openssl req -new -key applepay-ppc-ecc-256-private.key -out applepay-pcc-ecc-256.csr
   ```
   需要填写公司相关的信息，会得到 `applepay-pcc-ecc-256.csr` 文件。

#### 2.3.2 上传证书

1. 在 Merchant Id 详情页中的 **Apple Pay Payment Processing Certificate** 部分，点击 **Create Certificate** 创建证书
2. 选择上一步创建的CSR文件
3. 上传完成后点击 **Continue**
4. 成功后Apple会生成证书，点击 **Download** 下载证书

### 2.4 创建 Merchant Identity Certificate

调用Apple Pay的create session接口是SSL双向认证，需要使用客户端证书，就是Merchant Identity Certificate。

创建这个证书也需要生成私钥、CSR等步骤。

#### 2.4.1 生成私钥

这里是要生成RSA 2048的私钥：

```bash
openssl genrsa -out applepay-mic-rsa-2048-private.key 2048
```

得到 `applepay-mic-rsa-2048-private.key` 私钥文件，这个私钥需要保存好，后续在调用接口时会用到。

#### 2.4.2 生成 CSR

```bash
openssl req -new -key applepay-mic-rsa-2048-private.key -out applepay-mic-rsa-2048.csr
```

这里一样需要填写证书所有者的信息。填写完成后会得到 `applepay-mic-rsa-2048.csr` 文件。

#### 2.4.3 上传 CSR

1. 打开 Merchant Id 的详情页，找到 **Apple Pay Merchant Identity Certificate** 章节
2. 点击 **Create Certificate** 按钮，选择上一步生成的CSR文件后 **Continue**
3. 然后就能得到证书
4. 保存好证书，后续支付处理过程中会使用到

## 3. 集成步骤

> **注意**: 若商户已在自己收银台集成过Apple Pay，可直接按步骤3.4对接即可。

### 3.1 初始化页面时获取 Apple Pay Session

参考链接：
- [Creating an Apple Pay Session | Apple Developer](https://developer.apple.com/documentation/apple_pay_on_the_web/apple_pay_js_api/creating_an_apple_pay_session)
- [Requesting an Apple Pay payment session | Apple Developer](https://developer.apple.com/documentation/apple_pay_on_the_web/apple_pay_js_api/requesting_an_apple_pay_payment_session)

> **注意**: 在调用Apple的接口获取session时，需要使用到SSL的客户端证书，即前面创建的Merchant Identity Certificate。

### 3.2 用户支付获取 ApplePay Token

在session的 `onpaymentauthorized` 回调方法入参中可获取加密Token。

详情请参考：[onpaymentauthorized | Apple Developer](https://developer.apple.com/documentation/apple_pay_on_the_web/applepaysession/1778020-onpaymentauthorized)

```javascript
...
this.session = new window.ApplePaySession(APPLE_PAY_VERSION, this.payRequest);
...
this.session.onpaymentauthorized = (event) => {
  // event.payment.token 即为加密 token
};
...
```

拿到的 token 示例如下：

```json
{
  "paymentData": {
    "data": "",
    "signature": "",
    "header": {
      "publicKeyHash": "",
      "ephemeralPublicKey": "",
      "transactionId": ""
    },
    "version": "EC_v1"
  },
  "paymentMethod": {
    "displayName": "Visa 8007",
    "network": "Visa",
    "type": "debit"
  },
  "transactionIdentifier": ""
}
```

### 3.3 解密 Apple Pay Token

- Apple Pay Token的结构，详情请参考：[Payment token format reference | Apple Developer](https://developer.apple.com/documentation/passkit/apple_pay/payment_token_format_reference)
- 解密Token需要使用到前面创建的Payment Processing Certificate

解密后的data示例如下：

```json
{
  "applicationExpirationDate": "280228",
  "applicationPrimaryAccountNumber": "42710600003562",
  "currencyCode": "124",
  "deviceManufacturerIdentifier": "040010030273",
  "paymentData": {
    "eciIndicator": "5",
    "onlinePaymentCryptogram": "/wAAADcAv7mhHpQAAAAAgPdgE4A="
  },
  "paymentDataType": "3DSecure",
  "transactionAmount": "5564"
}
```

### 3.4 调用PayerMax进行支付

创建支付 `/orderAndPay` API 接口请求，其中关键字段：

- `paymentDetail.paymentMethodType`: `APPLEPAY`
- `paymentDetail.applePayPaymentData`: 为解密后的支付信息

#### 接口请求示例

将Apple Pay Token解密后的卡信息，传递给 `data.paymentDetail.applePayPaymentData` 字段中。

```json
{
  "version": "1.4",
  "keyVersion": "1",
  "requestTime": "2022-02-25T09:23:06.473+00:00",
  "appId": "6666c8b036a24579974497c2f9800001",
  "merchantNo": "020213834421234",
  "data": {
    "outTradeNo": "Test1645780876511",
    "subject": "this is subject",
    "totalAmount": 1,
    "currency": "AED",
    "country": "AE",
    "userId": "userId001",
    "integrate": "Direct_Payment",
    "expireTime": "1800",
    "paymentDetail": {
      "paymentMethodType": "APPLEPAY",
      "buyerInfo": {
        "firstName": "James",
        "lastName": "Smith",
        "phoneNo": "903124360628",
        "email": "james@google.com",
        "clientIp": "124.156.108.193",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
      },
      "applePayPaymentData": {
        "applicationExpirationDate": "2312",
        "applicationPrimaryAccountNumber": "4111111111111111",
        "currencyCode": "USD",
        "deviceManufacturerIdentifier": "A1B2C3D4",
        "paymentDataType": "3DSecure",
        "transactionAmount": "100.00",
        "paymentData": {
          "onlinePaymentCryptogram": "Aa0KZXFURkhF...",
          "eciIndicator": "07"
        },
        "network": "VISA",
        "type": "credit",
        "displayName": "Visa 0492"
      }
    },
    "goodsDetails": [
      {
        "goodsId": "D002",
        "goodsName": "Key buckle",
        "quantity": "2",
        "price": "0.5",
        "goodsCurrency": "AED",
        "showUrl": "http://ttt.com",
        "goodsCategory": "电脑"
      }
    ],
    "shippingInfo": {
      "firstName": "James",
      "lastName": "Smith",
      "phoneNo": "903124360628",
      "email": "xxx@google.com",
      "address1": "address1",
      "city": "GAZIOSMANPASA/ANKAR",
      "country": "TR",
      "zipCode": "06700"
    },
    "billingInfo": {
      "firstName": "James",
      "lastName": "Smith",
      "phoneNo": "903124360628",
      "email": "xxx@google.com",
      "address1": "address1",
      "city": "GAZIOSMANPASA/ANKAR",
      "country": "TR",
      "zipCode": "06700"
    },
    "riskParams": {
      "registerName": "lily",
      "regTime": "2023-07-01 12:08:34",
      "liveCountry": "VN",
      "payerAccount": "987654XXX",
      "payerName": "lily",
      "taxId": "1234567890"
    },
    "language": "en",
    "reference": "020213827524152",
    "terminalType": "WAP",
    "frontCallbackUrl": "https://xxx.com",
    "notifyUrl": "https://yyy.com"
  }
}
```

#### 接口响应示例

```json
{
  "code": "APPLY_SUCCESS",
  "msg": " Success.",
  "data": {
    "outTradeNo": "a1234934974321",
    "tradeToken": "T2025051210335071234567",
    "status": "SUCCESS"
  }
}
```
