# 支付 demo 需求冷启动

> **需求名称**: 支付 demo
> **需求编号**: REQ-20260227-001
> **创建日期**: 2026-02-27

---

## 一、需求背景与上下文

### 1.1 需求来源
本 demo 用于指导新人理解电商支付系统的核心设计，包括多渠道支付、支付对账、并发控制、退款处理等关键能力。

### 1.2 业务场景
电商购物支付系统，支持：
- 用户下单后选择微信或支付宝支付
- 高并发场景（秒杀、促销活动）
- 每日自动对账，确保资金安全
- 支持退款申请和退款处理

### 1.3 历史决策记录

| 日期 | 决策 | 原因 | 决策人 |
|------|------|------|-------|
| 2026-02-27 | 使用 Redis 实现幂等控制 | 性能高，支持分布式 | 系统设计 |
| 2026-02-27 | 使用消息队列异步处理支付 | 削峰填谷，提高并发能力 | 系统设计 |
| 2026-02-27 | 每日对账 + 差异告警 | 平衡性能和准确性 | 系统设计 |

---

## 二、核心概念与业务逻辑

### 2.1 支付渠道

#### 微信支付
- **适用场景**：小程序、公众号、APP、H5
- **核心接口**：
  - JSAPI支付（小程序/公众号）
  - Native支付（扫码）
  - H5支付
  - APP支付
- **回调机制**：支付成功后微信主动回调通知

#### 支付宝
- **适用场景**：网页、APP、扫码
- **核心接口**：
  - 手机网站支付
  - 电脑网站支付
  - APP支付
  - 当面付（扫码）
- **回调机制**：支付成功后支付宝主动回调通知

### 2.2 支付状态流转

``` text
待支付 ──支付成功──> 已支付 ──申请退款──> 已退款
   │                   │
   └──支付超时/取消──> 已关闭
```

| 状态 | 说明 | 允许操作 |
|------|------|---------|
| 待支付 | 订单创建，等待用户支付 | 支付、取消 |
| 已支付 | 支付成功，等待发货 | 退款 |
| 已关闭 | 超时或用户取消 | 无 |
| 已退款 | 退款完成 | 无 |

### 2.3 对账流程

``` text
┌─────────────────────────────────────────────────────┐
│                    每日对账任务                      │
└───────────────────────┬─────────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │ 下载微信  │  │ 下载支付宝│  │ 获取本地  │
    │ 账单数据  │  │ 账单数据  │  │ 订单数据  │
    └─────┬────┘  └─────┬────┘  └─────┬────┘
          │             │             │
          └─────────────┼─────────────┘
                        ▼
              ┌─────────────────┐
              │   数据比对      │
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ 时间差异  │  │ 金额差异  │  │ 记录差异  │
   │ 自动处理  │  │ 人工处理  │  │ 告警通知  │
   └──────────┘  └──────────┘  └──────────┘
```

### 2.4 并发控制策略

| 场景 | 控制方式 | 实现方案 |
|------|---------|---------|
| 防重复支付 | 幂等Key | Redis SETNX + 过期时间 |
| 防超卖 | 分布式锁 + 乐观锁 | Redisson + SQL条件更新 |
| 请求缓冲 | 消息队列 | RabbitMQ/Kafka |
| 数据一致 | 本地消息表 + 补偿 | 定时任务扫描 |

---

## 三、关键技术点

### 3.1 幂等性设计

**幂等Key设计规则**：

``` text
幂等Key = 业务标识:订单号:操作类型:时间窗口
示例：PAY:ORD202602270001:WECHAT:202602271430
```

**Redis 实现**：

``` java
public boolean acquireIdempotentKey(String key, int expireSeconds) {
    return Boolean.TRUE.equals(
        redisTemplate.opsForValue()
            .setIfAbsent(key, "1", expireSeconds, TimeUnit.SECONDS)
    );
}
```

### 3.2 分布式锁

**Redisson 使用示例**：

``` java
RLock lock = redissonClient.getLock("ORDER_PAY_LOCK:" + orderNo);
try {
    // 尝试获取锁，等待30秒，锁过期时间10秒
    if (lock.tryLock(30, 10, TimeUnit.SECONDS)) {
        // 处理支付逻辑
        processPayment(orderNo);
    } else {
        throw new BusinessException("获取锁超时");
    }
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    throw new BusinessException("获取锁中断");
} finally {
    if (lock.isHeldByCurrentThread()) {
        lock.unlock();
    }
}
```

**注意事项**：
- 必须设置锁过期时间，防止死锁
- 释放锁前检查是否持有锁
- 业务处理时间不应超过锁过期时间

### 3.3 金额处理

**数据库类型**：

``` sql
amount DECIMAL(10, 2) COMMENT '金额，单位：元'
```

**Java 类型**：

``` java
// 正确示例
private BigDecimal amount;

// 错误示例（禁止使用）
private Double amount;
private Float amount;
```

**金额计算**：

``` java
// 正确：使用 BigDecimal
BigDecimal total = price.multiply(quantity);
BigDecimal discount = amount.multiply(new BigDecimal("0.9"));

// 错误：使用浮点数运算（禁止）
double total = price * quantity;
```

### 3.4 回调处理

**回调验签示例（微信）**：

``` java
public boolean verifySign(String body, String signature, String serial) {
    // 1. 获取微信平台证书
    X509Certificate certificate = certificateService.getCertificate(serial);
    
    // 2. 验证签名
    Signature sign = Signature.getInstance("SHA256withRSA");
    sign.initVerify(certificate.getPublicKey());
    sign.update(body.getBytes(StandardCharsets.UTF_8));
    
    return sign.verify(Base64.getDecoder().decode(signature));
}
```

**幂等处理**：

``` java
public void handleCallback(PaymentCallback callback) {
    // 1. 幂等校验
    PaymentOrder order = orderMapper.selectByOrderNo(callback.getOrderNo());
    if (order.getStatus() == PaymentStatus.PAID) {
        // 已处理，直接返回成功
        return;
    }
    
    // 2. 分布式锁
    RLock lock = redisson.getLock("CALLBACK_LOCK:" + callback.getOrderNo());
    try {
        if (lock.tryLock(10, 5, TimeUnit.SECONDS)) {
            // 3. 更新订单状态
            orderMapper.updateStatus(callback.getOrderNo(), PaymentStatus.PAID);
            // 4. 记录支付流水
            paymentRecordMapper.insert(buildRecord(callback));
        }
    } finally {
        if (lock.isHeldByCurrentThread()) {
            lock.unlock();
        }
    }
}
```

---

## 四、常见问题与解决方案

### 4.1 问题1：支付回调丢失

**现象**：用户支付成功，但订单状态未更新

**原因**：
- 网络问题导致回调请求丢失
- 服务宕机导致回调未处理

**解决方案**：
1. 增加主动轮询机制：支付后定时查询第三方状态
2. 增加消息队列缓冲：回调先入队再处理
3. 定时补偿任务：扫描超时未支付订单

### 4.2 问题2：重复支付

**现象**：同一订单被多次支付

**原因**：
- 缺少幂等控制
- 分布式锁实现不当

**解决方案**：
1. 支付前设置幂等Key
2. 使用分布式锁保护支付逻辑
3. 数据库增加唯一约束

### 4.3 问题3：库存超卖

**现象**：库存不足但订单创建成功

**原因**：
- 库存扣减未加锁
- 数据库主从延迟

**解决方案**：
1. 使用 Redis 原子操作预扣库存
2. 数据库使用乐观锁
3. 秒杀场景使用消息队列削峰

### 4.4 问题4：对账差异

**现象**：本地订单与第三方账单不一致

**原因**：
- 跨日交易
- 手续费差异
- 交易状态不一致

**解决方案**：
1. 建立差异自动处理规则
2. 时间差异自动延后处理
3. 金额差异触发人工审核

---

## 五、测试验证清单

### 5.1 功能验证

- [ ] 微信支付成功，订单状态更新
- [ ] 支付宝支付成功，订单状态更新
- [ ] 支付回调正常处理
- [ ] 退款申请和退款处理正常
- [ ] 对账任务正常执行

### 5.2 并发验证

- [ ] 1000并发无重复支付
- [ ] 1000并发无订单丢失
- [ ] 秒杀场景无超卖
- [ ] 分布式锁无死锁

### 5.3 边界验证

- [ ] 金额边界（0.01元、大额）
- [ ] 网络超时处理
- [ ] 第三方服务不可用
- [ ] 并发锁超时

### 5.4 安全验证

- [ ] 签名验证通过
- [ ] 重放攻击防护
- [ ] 敏感信息加密

---

## 六、参考资源

### 6.1 官方文档
- [微信支付开发文档](https://pay.weixin.qq.com/wiki/doc/apiv3/apis/index.shtml)
- [支付宝开放平台](https://opendocs.alipay.com/apis/api_1/alipay.trade.page.pay)

### 6.2 相关文件
- 产品需求: [./产品/支付 demo.md](./产品/支付%20demo.md)
- 测试问题: [./测试/支付 demo测试问题.md](./测试/支付%20demo测试问题.md)

---

## 七、变更记录

| 日期 | 变更内容 | 变更人 |
|------|---------|-------|
| 2026-02-27 | 初始版本 | AI Assistant |

---

**注意**: 本文档随需求迭代持续更新，每次修改需记录变更历史。
