# 幂等性最佳实践

## 规则 14：数据库幂等性

**规则内容**：数据库操作必须实现幂等性 → 根据主键是否存在自动选择 insert 或 update → 思想：避免重复插入，确保数据一致性

## 概述

本文档记录了项目中幂等性设计的最佳实践和经验教训。

## 什么是幂等性

定义：同一个操作执行多次，产生的结果与执行一次相同。

**核心原则**：
- 数据库层面：根据主键是否存在，自动选择insert或update
- 接口层面：使用唯一标识（如taskId）避免重复处理
- 业务层面：通过状态机设计，确保同一状态不会重复处理

## 为什么需要幂等性

### 问题场景

在异步任务处理中，一个任务需要多次更新状态：

1. **创建任务记录**：首次插入，数据库自动生成主键
2. **更新任务状态为SUCCESS**：根据主键更新
3. **更新回调状态**：根据主键更新

### 错误示例

``` java
// 错误示例：每次都插入，导致主键重复
public boolean save(Entity entity) {
    int result = mapper.insert(entity);  // 每次都插入
    return result > 0;
}
```

**错误结果**：
``` text
Duplicate entry '5' for key 'llm_call_record.PRIMARY'
```

### 正确示例

``` java
// 正确示例：根据主键选择insert或update
public boolean save(Entity entity) {
    if (entity.getId() == null) {
        // 新增记录
        int result = mapper.insert(entity);
        return result > 0;
    } else {
        // 更新记录
        int result = mapper.updateById(entity);
        return result > 0;
    }
}
```

## 幂等性实现模式

### 模式1：基于主键的幂等性

**适用场景**：数据库操作，实体有主键

**实现方式**：
``` java
public boolean save(Entity entity) {
    if (entity.getId() == null) {
        // 新增记录
        int result = mapper.insert(entity);
        return result > 0;
    } else {
        // 更新记录
        int result = mapper.updateById(entity);
        return result > 0;
    }
}
```

**调用流程**：
``` java
// 首次调用：insert（id为null）
save(entity) → 插入记录 → 数据库自动生成id

// 后续调用：update（id已存在）
save(entity) → 更新记录 → 避免主键冲突
```

### 模式2：基于唯一标识的幂等性

**适用场景**：HTTP接口，使用唯一标识（如taskId）

**实现方式**：
``` java
@PostMapping("/api/llm/async")
public Result<LlmAsyncResponse> handleAsync(@RequestBody LlmAsyncRequest request) {
    // 生成任务ID
    String taskId = generateTaskId();

    // 检查任务是否已存在
    if (taskExists(taskId)) {
        return Result.success(getTaskResult(taskId));
    }

    // 创建新任务
    createTask(taskId, request);

    // 返回任务ID
    return Result.success(LlmAsyncResponse.success(taskId, request.getBusinessId()));
}
```

### 模式3：基于状态机的幂等性

**适用场景**：业务流程，通过状态机设计避免重复处理

**实现方式**：
``` java
public void updateTaskStatus(String taskId, String newStatus) {
    TaskEntity entity = taskMapper.selectById(taskId);

    // 检查当前状态
    if (entity.getStatus().equals(newStatus)) {
        // 状态相同，无需更新
        return;
    }

    // 检查状态流转是否合法
    if (!isValidStatusTransition(entity.getStatus(), newStatus)) {
        throw new IllegalStateException("非法的状态流转");
    }

    // 更新状态
    entity.setStatus(newStatus);
    taskMapper.updateById(entity);
}
```

## 幂等性规则

### 规则1：数据库操作必须实现幂等性

**来源**：`.ai/rule.md` 第10条规则

**内容**：
- save方法必须根据主键是否存在，自动选择insert或update
- 主键为null时执行insert，主键不为null时执行update
- 避免重复插入导致主键冲突（Duplicate entry错误）
- 异步任务的状态更新必须使用幂等性设计

**示例代码**：
``` java
public boolean save(Entity entity) {
    if (entity.getId() == null) {
        // 新增记录
        int result = mapper.insert(entity);
        return result > 0;
    } else {
        // 更新记录
        int result = mapper.updateById(entity);
        return result > 0;
    }
}
```

### 规则2：异步任务必须使用幂等性设计

**来源**：LlmAsyncServiceImpl实现经验

**内容**：
- 创建任务记录后，多次更新任务状态
- 每次更新都使用幂等性设计
- 避免重复插入导致主键冲突

**调用流程**：
``` java
// 1. 创建记录：insert（id为null）
save(entity) → 插入记录 → 数据库自动生成id

// 2. 更新成功状态：update（id已存在）
save(entity) → 更新记录 → 避免主键冲突

// 3. 更新回调状态：update（id已存在）
save(entity) → 更新记录 → 避免主键冲突
```

### 规则3：回调处理必须使用幂等性设计

**来源**：LlmAsyncServiceImpl回调经验

**内容**：
- 收到回调后，根据taskId更新任务状态
- 使用幂等性设计避免重复处理
- 记录回调次数，避免无限重试

**示例代码**：
``` java
private void callbackResult(String taskId, LlmAsyncRequest request, LLMResponse llmResponse, LlmCallRecordEntity entity) {
    try {
        // 构建回调数据
        LlmCallbackData callbackData = LlmCallbackData.builder()
                .taskId(taskId)
                .businessId(request.getBusinessId())
                .status("SUCCESS")
                .content(llmResponse.getContent())
                .build();

        // 发送HTTP回调
        boolean success = httpCallbackUtil.post(request.getCallbackUrl(), callbackData);

        if (success) {
            // 更新回调状态（幂等性）
            entity.setCallbackStatus("SUCCESS");
            entity.setCallbackTime(Instant.now());
            entity.setCallbackCount(entity.getCallbackCount() + 1);
            llmCallRecordService.save(entity);  // 使用幂等性save方法
        }
    } catch (Exception e) {
        log.error("HTTP回调异常，任务ID: {}", taskId, e);
    }
}
```

## 常见场景

### 场景1：异步任务

**描述**：创建任务记录后，多次更新任务状态

**实现方式**：
``` java
// 首次调用：insert（id为null）
save(entity) → 插入记录 → 数据库自动生成id

// 后续调用：update（id已存在）
save(entity) → 更新记录 → 避免主键冲突
```

### 场景2：订单处理

**描述**：创建订单后，多次更新订单状态

**实现方式**：
``` java
// 创建订单：insert
save(order) → 插入订单 → 数据库自动生成id

// 更新订单状态：update
save(order) → 更新订单 → 避免主键冲突
```

### 场景3：支付回调

**描述**：收到支付回调后，多次更新支付状态

**实现方式**：
``` java
// 首次回调：insert
save(payment) → 插入支付记录 → 数据库自动生成id

// 后续回调：update
save(payment) → 更新支付记录 → 避免主键冲突
```

## 注意事项

### 1. 幂等性设计需要考虑业务场景

**说明**：不是所有操作都适合幂等性

**示例**：
- ✅ 适合幂等性：创建任务、更新状态、回调处理
- ❌ 不适合幂等性：计数器、累加操作

### 2. 幂等性设计需要考虑并发场景

**说明**：使用乐观锁或悲观锁避免并发问题

**示例**：
``` java
// 乐观锁：使用版本号
public boolean save(Entity entity) {
    int result = mapper.updateById(entity);
    if (result == 0) {
        // 乐观锁冲突，重试
        return save(entity);
    }
    return result > 0;
}
```

### 3. 幂等性设计需要考虑性能影响

**说明**：避免不必要的更新操作

**示例**：
``` java
// 检查状态是否变化，避免不必要的更新
public void updateTaskStatus(String taskId, String newStatus) {
    TaskEntity entity = taskMapper.selectById(taskId);

    if (entity.getStatus().equals(newStatus)) {
        // 状态相同，无需更新
        return;
    }

    entity.setStatus(newStatus);
    taskMapper.updateById(entity);
}
```

## 经验教训

### 教训1：忽略幂等性导致主键冲突

**问题**：每次都使用insert，导致主键重复错误

**错误代码**：
``` java
public boolean save(Entity entity) {
    int result = mapper.insert(entity);  // 每次都插入
    return result > 0;
}
```

**错误结果**：
``` text
Duplicate entry '5' for key 'llm_call_record.PRIMARY'
```

**解决方案**：使用幂等性设计，根据主键选择insert或update

### 教训2：幂等性设计需要全局规范

**问题**：每个开发者都自己实现幂等性，导致代码不一致

**解决方案**：
- 在`.ai/rule.md`中添加幂等性规则
- 在`GLOBAL_CONCEPTS.md`中添加幂等性概念
- 提供统一的幂等性实现模式

### 教训3：幂等性设计需要考虑业务场景

**问题**：所有操作都使用幂等性，导致性能问题

**解决方案**：
- 根据业务场景选择是否使用幂等性
- 对于计数器、累加操作，不使用幂等性
- 对于创建、更新操作，使用幂等性

## 参考文档

- `@.iflow/context/concept/GLOBAL_CONCEPTS.md ` - 幂等性概念定义
- `@.iflow/context/rule/RULE_SPEC.md ` - 幂等性规则

---

**版本**: 1.0.0
**更新时间**: 2026-01-19
**维护者**: caas