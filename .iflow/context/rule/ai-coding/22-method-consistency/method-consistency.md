# 方法一致性

## 规则 17：方法一致性

**规则内容**：检查方法签名，确保方法参数一致 → 修改方法时同步更新所有调用点；思想：确保方法可以正确解析，使用 var 时类型必须明确

## 为什么需要方法一致性

确保方法可以正确解析，避免运行时错误，提高代码可读性，降低维护成本。

## 项目中的实际案例

### 案例1：LlmService.invokeLlm 方法签名变更

**变更前**：
``` java
public String invokeLlm(String prompt, String taskId) throws Exception {
    // ...
}
```

**变更后**：
``` java
public String invokeLlm(PromptContext promptContext, PromptTypeEnum promptTypeEnum) throws Exception {
    // ...
}
```

**需要同步更新的调用点**：
- `AbstractService.invokeMethod` - 已更新
- `LlmServiceImpl.invokeLlm` - 已更新

**结果**：所有调用点都已更新，编译通过。

### 案例2：WorkflowNodeExecutor.executeNode 方法

**方法签名**：
``` java
public NodeExecutionResult executeNode(WorkflowExecutionContext context, String nodeId)
```

**调用点**：
- `WorkflowManagerImpl.executeWorkflow` - 调用时必须提供 `context` 和 `nodeId`
- `WorkflowCallbackServiceImpl.handleCallback` - 调用时必须提供 `context` 和 `nodeId`

**一致性检查**：
- 参数类型必须完全匹配
- 参数顺序必须一致
- 返回值类型必须一致

### 案例3：WorkflowCallbackService.handleCallback 方法

**方法签名**：
``` java
void handleCallback(String workflowExecutionId, String nodeId, Object callbackData);
```

**调用点**：
- `LlmCallbackServiceImpl.handleCallback` - 调用时必须提供 `workflowExecutionId`、`nodeId`、`callbackData`
- `OcrCallbackServiceImpl.handleCallback` - 调用时必须提供 `workflowExecutionId`、`nodeId`、`callbackData`

**一致性检查**：
- 参数类型必须完全匹配
- 参数顺序必须一致
- 返回值类型必须一致

### 案例4：PromptBuilder.buildPrompt 方法

**方法签名**：
``` java
private String buildPrompt(List<PromptTemplate> templates)
```

**调用点**：
- `PromptBuilder.buildSystemPrompt` - 调用时必须提供 `systemTemplates`
- `PromptBuilder.buildUserPrompt` - 调用时必须提供 `userTemplates`

**一致性检查**：
- 参数类型必须完全匹配
- 参数顺序必须一致
- 返回值类型必须一致

## 常见错误案例

### 错误1：修改方法签名但未更新调用点

``` java
// 修改前
public User getUserById(Long userId) {
    return userRepository.findById(userId);
}

// 调用
User user = userService.getUserById(1L);

// 修改后
public User getUserById(Long userId, Boolean includeDetails) {
    return userRepository.findById(userId, includeDetails);
}

// 调用点未更新
User user = userService.getUserById(1L); // 编译错误
```

**问题**：修改方法签名后未更新调用点，导致编译错误。

### 错误2：使用 var 但类型不明确

``` java
// 类型不明确
var user = getUser(id); // 类型推断失败

// 应该使用显式类型
User user = getUser(id);
```

**问题**：使用 var 时类型不明确，导致类型推断失败。

### 错误3：参数顺序不一致

``` java
// 定义方法
public void processOrder(Long orderId, String status) {
    // ...
}

// 调用时参数顺序错误
processOrder("SUCCESS", 1L); // 编译错误
```

**问题**：调用时参数顺序错误，导致编译错误。

## 如何检查

### 检查清单
- [ ] 修改方法签名后是否同步更新了所有调用点？
- [ ] 使用 var 时类型是否明确？
- [ ] 方法参数类型是否正确？
- [ ] 方法参数顺序是否一致？
- [ ] 方法返回值类型是否正确？

### 检查方法

#### 方法1：编译检查
运行 `mvn compile` 检查是否有编译错误。

#### 方法2：使用 IDE 的查找功能
使用 IDE 的查找功能，查找所有调用点，确保所有调用点都已更新。

#### 方法3：使用 IDE 的重命名和重构功能
使用 IDE 的重命名和重构功能，确保所有调用点都被更新。

## 常见误区

1. **以为修改方法签名很简单**：必须同步更新所有调用点
2. **以为 var 可以用于所有情况**：泛型类型必须使用显式类型声明
3. **以为编译器会自动推断**：类型必须明确，不能有歧义

## 最佳实践

### 实践1：使用 IDE 的重命名和重构功能
使用 IDE 的重命名和重构功能，确保所有调用点都被更新。

### 实践2：泛型类型使用显式类型声明

``` java
// 泛型类型必须使用显式类型声明
Map<String, List<User>> userMap = new HashMap<>();

// 不能使用 var（类型不明确）
var userMap = new HashMap<String, List<User>>();
```

### 实践3：编译验证
修改方法签名后必须运行编译检查，确保没有编译错误。

### 实践4：参数对象设计
如果方法参数过多，考虑使用参数对象：

``` java
// 不推荐：参数过多
public void processOrder(Long orderId, String status, Long userId, String userName, String address, ...) {
    // ...
}

// 推荐：使用参数对象
public void processOrder(OrderProcessRequest request) {
    // ...
}
```

### 实践5：使用 @Override 注解
使用 @Override 注解可以确保方法签名正确：

``` java
@Override
public String invokeLlm(PromptContext promptContext, PromptTypeEnum promptTypeEnum) throws Exception {
    // ...
}
```

**优点**：
- 编译器会检查方法签名是否正确
- 如果父类方法签名变更，编译会失败，提醒你更新子类