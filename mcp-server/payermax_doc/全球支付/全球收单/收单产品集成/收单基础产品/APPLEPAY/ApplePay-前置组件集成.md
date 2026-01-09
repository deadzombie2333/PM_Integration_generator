# ApplePay-前置组件集成

该文档介绍前置组件下，使用Apple Pay的集成要求。

## 1. 集成说明

该模式下商户集成和前置组件支付通用流程基本一致。

商户收银页面集成PayerMax提供的ApplePay前端接口，用户无需跳转至PayerMax收银台页面，减少跳转流程。

同时，ApplePay证书统一由PayerMax维护，商户仅需下载ApplePay认证文件保存在指定位置即可。

## 2. 域名认证配置步骤

### 步骤1：提供域名信息

联系PayerMax技术支持，提供您的正式环境和测试环境的域名，以完成Apple的域名认证要求。

> **特别注意**: 在测试环境中，`127.0.0.1`、局域网IP、`localhost` 都无法拉起ApplePay。

### 步骤2：下载并配置认证文件

下载ApplePay认证文件，并放置在指定路径：

```
https://[待注册域名]/.well-known/apple-developer-merchantid-domain-association
```

**认证文件下载：**
- **测试环境认证文件**: [apple-developer-merchantid-domain-association](测试环境下载链接)
- **生产环境认证文件**: [apple-developer-merchantid-domain-association](生产环境下载链接)

### 步骤3：通知PayerMax验证

商户配置好证书后，通知PayerMax验证域名证书，PayerMax将在Apple开发者后台操作域名证书验证。

## 3. 验证失败排查

如果验证失败，可能的原因如下：

1. **证书路径配置错误**
   - 确保文件放置在正确的路径：`/.well-known/apple-developer-merchantid-domain-association`

2. **防火墙拦截**
   - 您的防火墙拦截了苹果检查服务
   - 请配置链接页面域名至服务器白名单

3. **已配置其他MerchantID证书**
   - 可能已经配置过其他MerchantID的证书
   - 解决方案：
     - 使用新域名，或
     - 在原开发者账号上删除对应域名证书

## 4. 前端集成

商户收银页面集成PayerMax提供的ApplePay前端接口，具体请查看前置组件支付文档。
