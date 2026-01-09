# ISV服务商接入

## 1. ISV是什么

ISV全称为"Independent Service Provider",在PayerMax内部,推荐自身拥有子商户资源的支付机构或SaaS服务商以ISV的身份接入。

ISV与PayerMax完成系统集成后,可以代子商户发起交易请求。

## 2. 适用场景

ISV本身可以是拥有支付牌照的机构,也可以是SaaS服务提供商,在采用ISV模式与PayerMax对接之前,请先联系对接商务确认业务场景和用户流程是否合适。

## 3. 流程和角色关系

## 4. 支持集成模式

通过ISV模式接入PayerMax的商户,在支持的集成模式上与普通商户无区别,即支持收银台支付、纯API支付、前置组件、链接支付、Tokenization支付。

## 5. 接口参数

在ISV模式下,ISV作为集成方需要关注几个核心参数：

- **spMerchantNo**：指ISV商户自身的商户号,在以ISV身份入驻PayerMax时由PayerMax分配。

- **merchantNo**：指子商户的商户号。子商户一般也需要在PayerMax入驻,入驻时由PayerMax分配,并提供给ISV商户在每次发起交易时传入。

- **appId**：代表的是系统集成方的应用,密钥与appId绑定。对于ISV服务商,系统集成由ISV服务商来集成,所以交易接口中的appId上送的是ISV服务商的appId。

- **Auth Token**：当ISV商户和其子商户分别在PayerMax完成入驻后,PayerMax会基于二者的绑定关系生成Auth Token。如果一个ISV存在多个子商户,则PayerMax会分配多个Auth Token区分来自不同子商户的交易。ISV服务商在代子商户请求交易时,在HTTP Header中上送`merchant_auth_token=授权分配的Auth Token`。

## 6. 传参指引

### 请求Header：

传入`merchant_auth_token`,示例如下：

```json
{
  "headers": {
    "Accept": "application/json",
    "merchant_auth_token": "2024071***73504",  //必须
    "sign": "请参考签名规则：https://docs-v2.payermax.com/doc-center/developer/config-settings.html",  //必须
    "Content-Type": "application/json"
  }
}
```

### 请求Body：

示例如下,详细的接口文档请参阅收银台-下单接口。

**注意**：接口中没有spMerchantNo,请参考下面Body。

```json
{
  "requestTime": "2024-08-12T14:59:53.279+08:00",
  "version": "1.1",
  "appId": "需要替换为ISV服务商的appid",
  "merchantNo": "需要替换为子商户号",
  "spMerchantNo": "需要替换为ISV服务商商户号",
  "keyVersion": "1",
  "data": {
    "outTradeNo": "20240812025xxxx",
    "userId": "704138842",
    "subject": "商品描述",
    "totalAmount": 700,
    "country": "KR",
    "currency": "KRW",
    "language": "en",
    "frontCallbackURL": "https://www.baidu.com",
    "notifyUrl": "https://www.baidu.com"
  }
}
```

### 参数说明：

| 参数 | 类型 | 是否必填 | 最大长度 | 描述 | 示例值 |
|------|------|---------|---------|------|--------|
| version | String | M | 8 | 接口版本。当前值为：1.1 | 1.1 |
| keyVersion | String | M | 8 | 密钥版本。当前值为：1 | 1 |
| requestTime | String | M | 32 | 请求时间,符合rfc3339规范,格式：yyyy-MM-dd'T'HH:mm:ss.SSSXXX | 2022-01-22T10:00:00.500+08:00 |
| appId | String | M | 64 | 集成方的集成App Id | 46153e2b787241ae8b01857bb087d1bd |
| spMerchantNo | String | M | 15 | ISV服务商的商户号 | |
| merchantNo | String | M | 15 | 商户号,商户与PayerMax业务签约时生成的唯一标识 | 010229810189301 |
| +data | Object | | | 请参见各业务接口下的具体字段 | |
