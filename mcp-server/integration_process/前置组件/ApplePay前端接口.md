# ApplePay前端接口

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
| applepay | string | ApplePay组件 |

### Options详解

| Options | 是否必填 | 字段类型 | 描述 | 默认值 |
|---------|---------|---------|------|--------|
| clientKey | Y | String | 客户端公钥 | - |
| sessionKey | Y | String | 安全访问令牌 | - |
| sandbox | N | Boolean | 沙盒环境 | false |
| theme | N | String | 主题 | light |
| payButtonStyle | N | String | 按钮样式 | - |

## 1.2 mount

用于挂载初始化组件实例，使用方法：`PMdropin.mount(Tag)`

### Tag详解

| Tag | 描述 |
|-----|------|
| id | 需要挂载的id元素值，如 `PMdropin.mount('#applepay-frame')` |
| class | 需要挂载的class元素值，如 `PMdropin.mount('.applepay-frame')` |

## 1.3 on

用于监听组件内置响应事件，使用方法：`PMdropin.on(Event, CallbackFunction)`

### Event详解

| Tag | 描述 | 返回值 |
|-----|------|--------|
| ready | 组件加载完成时触发 | null |
| payButtonClick | ApplePay按钮被点击时触发 | null |

### 示例

```javascript
PMdropin.on('payButtonClick', function(event) {
  // achieve paymentToken and orderAndPay
  applePay.emit('setDisabled', true)
  
  applePay.emit('canMakePayment').then(res => {
    const paymentToken = res?.data?.paymentToken 
    
    if(paymentToken){
      orderAndPay()
    } else { 
      applePay.emit('setDisabled', false)
    }
  }).catch(err => {
    applePay.emit('payFail')
    applePay.emit('setDisabled', false) 
  })
});
```

## 1.4 emit

用于调用组件内置方法，使用方法：`PMdropin.emit(Event, Params)`

| Event | Params | 描述 |
|-------|--------|------|
| canMakePayment | - | 获取本次支付token |
| switchTheme | string | 切换主题 |
| setDisabled | Boolean | 设置组件可用状态 |
| setPayButtonStyle | string | 设置按钮样式 |

### 1.4.1 emit.canMakePayment

检查当前组件状态是否具备发起支付条件，如果校验通过则返回卡标识。

#### Options配置

| Options | 是否必填 | 字段类型 | 描述 | 默认值 |
|---------|---------|---------|------|--------|
| totalAmount | N | String | ApplePay支付页面展示金额<br>数字字符串，最多传入两位小数，如果传入非法值canMakePayment响应会抛出异常AMOUNT_INVALID<br>**注**：该场景仅仅适用于applyDropinSession不传金额的场景，如果applyDropinSession传入了金额，不要使用该能力，务必确保canMakePayment传入的 totalAmount和最终支付orderAndPay传入的金额保持一致 | - |

#### canMakePayment Response

| Code码 | 描述 |
|--------|------|
| APPLY_SUCCESS | 成功获取 paymentToken |
| UNKNOWN_ISSUE | 异常信息 |
| AMOUNT_INVALID | 传入金额格式有误 |
| APPLEPAY_INTERNAL_ERROR | Apple Pay 内部异常 |

### 1.4.2 emit.switchTheme

设置按钮主题

- 类型：String
- 默认：light

| 主题名称 | 主题编码 | 效果预览 |
|---------|---------|---------|
| 白色 | light (默认) | ![白色主题](https://example.com/light-theme.png) |
| 黑色 | dark | ![黑色主题](https://example.com/dark-theme.png) |

### 1.4.3 emit.setDisabled

设置组件可用状态

- 类型：Boolean
- 默认：false

```javascript
// 按钮不可用状态
PMdropin.emit('setDisabled', true)

// 按钮可用状态
PMdropin.emit('setDisabled', false)
```

### 1.4.4 emit.setPayButtonStyle

设置按钮样式

- 类型：String
- 默认：-

```javascript
// 设置ApplePay按钮宽高、内边距、边框弧度
PMdropin.emit('payButtonStyle', `width:20rem;height:4rem;border-radius: 4rem;padding:1rem 4rem;`)
```
