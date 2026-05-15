# Application Legibility（应用可读性）

> **定位**: 代码不仅要对人可读，更要对 Agent 可读
> **来源**: Harness Engineering（驾驭工程）核心原则
> **L2 引用**: @.iflow/ecosystem/rule/ai-coding/CODING_SPEC.md

---

## 定义

**Application Legibility** 是指代码和文档的"可被 AI Agent 理解"的程度。传统的代码可读性关注人类开发者，而 Application Legibility 关注的是 AI Agent 能否准确理解代码结构、意图和约束。

**核心原则**：
- **显式优于隐式**：Agent 不擅长理解隐含约定
- **结构优于注释**：Agent 更依赖结构化线索
- **一致优于灵活**：一致的模式降低理解成本

---

## 为什么重要

| 对比维度 | 人类开发者 | AI Agent |
|---------|-----------|---------|
| **理解方式** | 结合上下文 + 常识推理 | 纯文本模式匹配 |
| **隐含约定** | 能理解"一看就懂"的约定 | 盲区，容易误解 |
| **一致性要求** | 可以适应不同风格 | 需要一致模式 |
| **文档依赖** | 可选择性阅读 | 必须显式告知 |

---

## 使用场景

- **场景1**：AI 编写代码时，需要理解现有代码结构
- **场景2**：AI 审查代码时，需要识别代码意图
- **场景3**：AI 重构代码时，需要确保不破坏隐含逻辑
- **场景4**：设计 AI 可读的项目结构时

---

## 核心原则

### 1. 显式优于隐式

| 隐式（不利于 Agent）| 显式（有利于 Agent）|
|-------------------|-------------------|
| 魔法数字 `86400` | 常量 `SECONDS_PER_DAY` |
| 隐含的返回值 | 显式的类型定义 |
| 约定俗成的命名 | 一致的命名规范 |
| 注释解释代码 | 代码自解释 |

### 2. 结构优于注释

| 注释驱动（不利于 Agent）| 结构驱动（有利于 Agent）|
|-----------------------|-----------------------|
| `// 这是一个服务类` | `class XxxService` |
| `// 这个方法返回用户` | `User getUser()` |
| 复杂的注释块 | 清晰的方法签名 |

### 3. 一致优于灵活

| 灵活但不一致（不利于 Agent）| 一致的模式（有利于 Agent）|
|--------------------------|--------------------------|
| 各种命名风格 | 统一命名规范 |
| 多种错误处理方式 | 统一异常处理模式 |
| 混合的代码风格 | 一致的代码风格 |

---

## 示例

### ❌ 不利于 Agent 的代码

```java
// 处理用户
public Object process(Object input) {
    if (input == null) return null;
    // ... 复杂逻辑
    return result;
}
```

### ✅ 有利于 Agent 的代码

```java
/**
 * 处理用户请求，返回处理结果
 *
 * @param request 用户请求，不能为 null
 * @return 处理结果，不会返回 null
 * @throws IllegalArgumentException 如果请求无效
 */
public ProcessResult processUserRequest(UserRequest request) {
    Objects.requireNonNull(request, "request cannot be null");
    // ... 清晰逻辑
    return ProcessResult.success(result);
}
```

---

## 与 .iflow 的关联

| .iflow 组件 | Application Legibility 体现 |
|------------|---------------------------|
| **IFLOW.md** | ≤60 行目录索引，结构清晰 |
| **CONCEPT_SPEC.md** | 触发条件映射表，显式关联 |
| **rule/** | 规则编号 + 命名规范，一致模式 |
| **experience/** | 场景标签 + 解决方案，结构化沉淀 |

---

## L2 详细内容

- **编码规范**: `@.iflow/ecosystem/rule/ai-coding/CODING_SPEC.md`
- **命名语义**: `@.iflow/ecosystem/rule/ai-coding/27-naming-semantic.md`
- **方法论**: `@.iflow/ecosystem/methodology/method-index.md`

---

## AI 执行检查

| 检查项 | 合格标准 | 不合格示例 |
|-------|---------|-----------|
| **显式原则** | 代码显式表达意图 | 使用魔法数字、隐含约定 |
| **结构清晰** | 结构化线索明确 | 依赖注释解释代码 |
| **一致性** | 遵循项目统一模式 | 同一功能用不同风格 |

**AI自检模板**：

```text
### 应用可读性检查
| 检查项 | 是否合格 | 说明 |
|-------|---------|------|
| 显式原则 | ✅/❌ | 是否显式: ... |
| 结构清晰 | ✅/❌ | 结构是否清晰: ... |
| 一致性 | ✅/❌ | 是否符合项目模式: ... |
```

---

**最后更新**：2026-03-23
**来源**：Harness Engineering（驾驭工程）
**关键词**：显式、结构、一致、AI 可读
