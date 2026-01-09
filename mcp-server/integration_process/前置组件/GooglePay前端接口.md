# GooglePay前端接口

## 1. API使用方法

PMdropin.API

| API | 描述 | 详情 |
|-----|------|------|
| create | 示例化一个内置组件 | 参阅 [create](#11-create) |
| mount | 将实例化组件挂载到div标签 | 参阅 [mount](#12-mount) |
| on | 监听事件 | 参阅 [on](#13-on) |
| emit | 触发事件 | 参阅 [emit](#14-emit) |

## 1.1 create

用于初始化组件，使用方法：`PMdropin.create(ComponentName, Options)`

### ComponentName详解

| ComponentName | 字段类型 | 描述 |
|--------------|---------|------|
| googlepay | string | GooglePay组件 |

### Options详解

| Options | 是否必填 | 字段类型 | 描述 | 默认值 |
|---------|---------|---------|------|--------|
| clientKey | Y | String | 客户端公钥 | - |
| sessionKey | Y | String | 安全访问令牌 | - |
| sandbox | N | Boolean | 沙盒环境 | false |
| payButtonStyle | N | Object | 按钮样式 | `{buttonRadius: "12", buttonColor: "default", buttonType: "plain", buttonLocale: "en", width: "240px", height: "40px"}` |

## 1.2 mount

用于挂载初始化组件实例，使用方法：`PMdropin.mount(Tag)`

### Tag详解

| Tag | 描述 |
|-----|------|
| id | 需要挂载的id元素值，如 `PMdropin.mount('#googlepay-frame')` |
| class | 需要挂载的class元素值，如 `PMdropin.mount('.googlepay-frame')` |

## 1.3 on

用于监听组件内置响应事件，使用方法：`PMdropin.on(Event, CallbackFunction)`

### Event详解

| Tag | 描述 | 返回值 |
|-----|------|--------|
| ready | 组件加载完成时触发 | null |
| payButtonClick | GooglePay按钮被点击时触发 | null |

## 1.4 emit

用于调用组件内置方法，使用方法：`PMdropin.emit(Event, Params)`

| Event | Params | 描述 |
|-------|--------|------|
| canMakePayment | - | 获取本次支付token |
| switchTheme | string | 切换主题 |
| setDisabled | Boolean | 设置组件可用状态 |
| setPayButtonStyle | Object | 设置按钮样式 |

### 1.4.1 emit.canMakePayment

检查当前组件状态是否具备发起支付条件，如果校验通过则返回卡标识。

#### Options配置

| Options | 是否必填 | 字段类型 | 描述 | 默认值 |
|---------|---------|---------|------|--------|
| totalAmount | N | String | GooglePay支付页面展示金额<br>数字字符串，最多传入两位小数，如果传入非法值canMakePayment响应会抛出异常AMOUNT_INVALID<br>**注**：该场景仅仅适用于applyDropinSession不传金额的场景，如果applyDropinSession传入了金额，不要使用该能力，务必确保canMakePayment传入的 totalAmount和最终支付orderAndPay传入的金额保持一致 | - |

#### canMakePayment Response

| Code码 | 描述 |
|--------|------|
| APPLY_SUCCESS | 成功获取 paymentToken |
| UNKNOWN_ISSUE | 异常信息 |
| AMOUNT_INVALID | 传入金额格式有误 |

### 1.4.2 emit.setDisabled

设置组件可用状态

- 类型：Boolean
- 默认：false

```javascript
// 按钮不可用状态
PMdropin.emit('setDisabled', true)

// 按钮可用状态
PMdropin.emit('setDisabled', false)
```

### 1.4.3 emit.setPayButtonStyle

设置按钮样式

- 类型：Object
- 默认：

```javascript
{
  buttonRadius: "12",      // 设置googlepay按钮边框弧度 String
  buttonColor: 'default',  // 设置按钮颜色  "default"/"white"/"black"
  buttonType: 'plain',
  buttonLocale: 'en',
  width: "240px",
  height: "40px",
}
```

## 2. 内部字段说明

| 字段 | 默认值 | 类型 | 枚举值 | 功能说明 |
|-----|--------|------|--------|---------|
| width | "240px" | String | / | 设置googlepay按钮宽 |
| height | "40px" | String | / | 设置googlepay按钮高 |
| buttonRadius | "12" | String | / | 设置googlepay按钮边框弧度 |
| buttonColor | 'default' | String | 'default'/'white'/'black' | 设置按钮颜色 |
| buttonType | 'plain' | String | "plain", "buy", "book", "checkout", "donate", "order", "pay", "subscribe" | 设置按钮类型，同GooglePay官方。[自定义按钮预览demo](https://developers.google.com/pay/api/web/guides/resources/customize) |
| buttonLocale | 'en' | String | 'en'/'ja'/'zh'/... 国际语种编码 | 设置按钮上文案的多语言，同GooglePay官方，需指定类型才支持，如"checkout"、"donate"等 |

## 3. 颜色展示

| 入参 | 效果预览 |
|-----|---------|
| default | ![default](https://example.com/googlepay-default.png) |
| white | ![white](https://example.com/googlepay-white.png) |
| black | ![black](https://example.com/googlepay-black.png) |

## 4. buttonType展示

| 入参 | 效果预览 |
|-----|---------|
| "plain" | ![plain](https://example.com/googlepay-plain.png) |
| "buy" | ![buy](https://example.com/googlepay-buy.png) |
| "book" | ![book](https://example.com/googlepay-book.png) |
| "checkout" | ![checkout](https://example.com/googlepay-checkout.png) |
| "donate" | ![donate](https://example.com/googlepay-donate.png) |
| "order" | ![order](https://example.com/googlepay-order.png) |
| "pay" | ![pay](https://example.com/googlepay-pay.png) |
| "subscribe" | ![subscribe](https://example.com/googlepay-subscribe.png) |

## 5. buttonLocale展示

| 入参 | 效果预览 | 说明 |
|-----|---------|------|
| "ja" | ![Japanese](https://example.com/googlepay-ja.png) | Japanese |
| "bg" | ![Bulgarian](https://example.com/googlepay-bg.png) | Bulgarian |
