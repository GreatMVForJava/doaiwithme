# Javadoc注释

## 规则 11：Javadoc注释

**规则内容**：每一个操作都需要按照 javadoc 规范写好注释 → 包括创建原因、使用场景、设计思想、对应边界，禁止使用行尾注释，以行间注释说明；思想：注释是代码的一部分，帮助理解设计意图和边界

## 为什么需要 Javadoc 注释

帮助理解设计意图和边界，提高代码可读性，降低维护成本，便于 IDE 自动生成文档。

## 项目中的实际案例

### 好的示例（符合规范）

#### 示例1：PromptBuilder.buildPrompt 方法

``` java
/**
 * 构建Prompt（公共方法）
 * 创建原因：buildSystemPrompt 和 buildUserPrompt 有大量重复代码，提取公共方法
 * 使用场景：构建 System 或 User Prompt
 * 设计思想：统一构建逻辑，减少代码重复
 *
 * @param templates 模板列表
 * @return Prompt字符串
 */
private String buildPrompt(List<PromptTemplate> templates) {
    // ...
}
```

**评价**：完整的 Javadoc，包含创建原因、使用场景、设计思想、参数说明、返回值说明。

#### 示例2：PromptBuilder.appendWithSeparator 方法

``` java
/**
 * 追加内容并添加分隔符
 * 创建原因：消除硬编码的分隔符 "\n\n"
 * 使用场景：构建多个模板时，在模板之间添加分隔符
 * 设计思想：使用常量定义分隔符，便于统一修改
 *
 * @param sb StringBuilder
 * @param content 要追加的内容
 */
private void appendWithSeparator(StringBuilder sb, String content) {
    // ...
}
```

**评价**：完整的 Javadoc，说明了创建原因、使用场景、设计思想。

#### 示例3：AbstractService.invoke 方法

``` java
/**
 * 封装LLM服务调用逻辑，统一异常处理
 * 创建原因：封装LLM服务调用逻辑，统一异常处理
 * 使用场景：LLM节点处理器调用LLM服务
 * 设计思想：将异常处理逻辑封装，避免子类重复实现
 * 对应边界：调用前检查任务状态，调用后处理异常
 *
 * @param promptContext Prompt上下文
 * @param promptTypeEnum Prompt类型枚举
 * @return LLM返回内容
 * @throws Exception LLM调用异常
 */
protected String invokeLlm(PromptContext promptContext, PromptTypeEnum promptTypeEnum) throws Exception {
    // ...
}
```

**评价**：完整的 Javadoc，包含对应边界说明。

### 错误示例（违反规范）

#### 错误1：注释过于简略

``` java
// ❌ 错误：注释过于简略
public User getUserById(Long userId) {
    return userRepository.findById(userId);
}
```

**问题**：没有说明创建原因、使用场景、设计思想、对应边界。

#### 错误2：使用行尾注释

``` java
// ❌ 错误：使用行尾注释
public User getUserById(Long userId) { // 根据用户ID获取用户
    return userRepository.findById(userId);
}
```

**问题**：使用行尾注释，违反了规范。

#### 错误3：注释不准确

``` java
// ❌ 错误：注释与实际不符
/**
 * 根据用户名获取用户
 */
public User getUserById(Long userId) {
    return userRepository.findById(userId);
}
```

**问题**：注释说"根据用户名获取用户"，但实际是"根据用户ID获取用户"。

#### 错误4：缺少对应边界说明

``` java
// ❌ 错误：缺少对应边界说明
/**
 * 更新节点状态为成功
 * @param caseId 任务ID
 */
public void markNodeAsSuccess(Long caseId) {
    // ...
}
```

**问题**：没有说明对应边界（如节点必须已存在、状态必须为 PENDING）。

## 如何检查

### 检查清单
- [ ] 是否使用了 Javadoc 格式（/** ... */）？
- [ ] 是否包含了创建原因？
- [ ] 是否包含了使用场景？
- [ ] 是否包含了设计思想？
- [ ] 是否包含了对应边界（如果有）？
- [ ] 是否使用了行间注释而非行尾注释？

### Javadoc 格式

``` java
/**
 * [方法/类的简要说明]
 *
 * 创建原因：[说明为什么创建这个方法/类]
 * 使用场景：[说明在什么场景下使用]
 * 设计思想：[说明设计思路和实现方式]
 * 对应边界：[说明边界条件和限制]
 *
 * @param [参数名] [参数说明]
 * @return [返回值说明]
 * @throws [异常类型] [异常说明]
 */
```

## 常见误区

1. **以为简单的代码不需要注释**：所有公共方法都需要注释
2. **以为只需要说明"做什么"**：还需要说明"为什么做"、"怎么做"、"边界是什么"
3. **以为行尾注释也可以**：必须使用 Javadoc 格式
4. **以为注释越多越好**：注释应该简洁明了，避免废话

## 最佳实践

### 实践1：使用标准 Javadoc 格式

``` java
/**
 * 构建单个模板
 * 创建原因：封装模板构建逻辑，统一处理模板渲染
 * 使用场景：构建系统提示词和用户提示词
 * 设计思想：通过模板引擎渲染模板，支持变量替换
 * 对应边界：模板必须存在，上下文数据不能为空
 *
 * @param template Prompt模板
 * @param context 上下文数据
 * @return 构建后的内容
 */
private String buildTemplate(PromptTemplate template, Map<String, Object> context) {
    return template.build(context);
}
```

### 实践2：使用行间注释说明复杂逻辑

``` java
public void processOrder(Order order) {
    // 校验订单状态
    if (order.getStatus() != OrderStatus.PENDING) {
        throw new IllegalArgumentException("订单状态不正确");
    }

    // 扣减库存
    inventoryService.deduct(order.getProductId(), order.getQuantity());

    // 创建支付记录
    paymentService.createPayment(order);

    // 更新订单状态
    order.setStatus(OrderStatus.PAID);
    orderRepository.save(order);
}
```

### 实践3：注释要简洁明了

避免废话，直奔重点，只包含必要信息。项目中的注释风格已经统一，参考 `XxxService`、`AbstractService` 等类的注释风格。