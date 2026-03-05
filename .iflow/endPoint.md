# endPoint.md - AI 执行规范

---

## 零、核心流程

``` text
预检 → 确认 → 规划 → 执行 → 自检 → 沉淀
```

每步都必须输出，等待人类确认。

**详细流程**：见 `@.iflow/context/rule/ai-collaboration/workflow/WORKFLOW_SPEC.md `

---

## 一、预检

**核心问题：是否有概念阻塞？这是什么类型的操作？需要读取哪些文件？**

**执行顺序**：
1. **概念阻塞检查**：是否有不理解的概念？→ 先读取 `@.iflow/context/concept/GLOBAL_CONCEPTS.md`
2. **意图判断**：根据理解的需求，判断操作意图
3. **文件读取**：根据意图映射必须读取的文件列表

**意图-文件映射表**：

| 操作意图 | 必须读取的文件 |
|---------|---------------|
| 修改规范文件 | `@.iflow/start.md `, `@.iflow/endPoint.md `, 相关规范文件 |
| 修改代码文件 | `@.iflow/context/rule/ai-coding/CODING_SPEC.md `, 相关代码文件 |
| 沉淀经验 | `@.iflow/context/experience/collaboration-method.md `, `@.iflow/context/experience/EXPERIENCE_SPEC.md ` |
| 创建文档 | 检查规则8，确认是否允许 |

**人机协作**：AI 自行判断意图，有概念阻塞则主动消除

**输出格式**：
```
## 预检
- 概念阻塞：[无 / 有，概念：xxx，已读取：@GLOBAL_CONCEPTS.md，已理解：xxx]
- 操作意图：[修改规范/修改代码/沉淀经验/创建文档]
- 必须读取：
  - @.iflow/context/xxx/xxx.md 
  - @.iflow/context/xxx/xxx.md 
- 已读取摘要：
  - @文件1：核心内容概述
  - @文件2：核心内容概述
```

---

## 二、关键操作检查点

以下操作必须在执行前输出检查，等待人类确认：

| 关键操作 | AI必须输出 | 人类介入 |
|---------|-----------|---------|
| **创建 md 文件** | "检查规则8，是否允许创建？" | 必须确认 |
| **git commit** | "检查规则6，是否允许提交？" | 必须确认 |
| **git push** | "检查规则6，是否允许推送？" | 必须确认 |
| **任务完成自检** | 输出完整规则检查表 | 必须确认 |

**详细规范**：见 `@.iflow/context/rule/ai-collaboration/checkpoint/CHECKPOINT_SPEC.md `

---

## 三、执行流程图

``` text
预检 → [概念阻塞？] → 有阻塞 → 调用skill/确认 → 消除阻塞
          ↓ 无阻塞
确认 → [输出需求理解] → 用户确认？
                              ↓ 是
规划 → [输出检查清单+计划] → 用户确认？
                              ↓ 是
执行 → [输出修改列表+编译]
        ↓
        关键操作？ → 创建md/git commit/git push → 输出检查 → 用户确认？
                              ↓ 是                              ↓ 是
自检 → [输出完整规则检查表] → 用户确认？
                              ↓ 是
沉淀 → [输出沉淀内容+路径] → 用户确认 → 执行
```

---

## 四、核心步骤

### 4.0 预检
**必须输出**：概念阻塞检查结果

**执行内容**：
- 检查是否有概念阻塞理解需求
- 有阻塞则调用 skill 查询或向用户确认

**人机协作**：AI 自行判断，有阻塞则主动消除

### 4.1 确认
**必须输出**：需求理解复述 + 理解边界

**执行内容**：
- 复述用户需求："我理解您需要..."
- 说明理解边界：包含什么、不包含什么
- 识别模糊点：需要进一步确认的内容

**人机协作**：AI 输出理解 → 人类确认或纠正

### 4.2 规划
**必须输出**：联动检查清单 + 执行计划

**执行内容**：
- 复用历史经验：读取 issues/ 和 experience/
- 联动检查：识别数据流上下游、共享概念、文档同步
- 执行计划：列出待修改文件、待删除文件、风险点

**人机协作**：AI 输出规划 → 人类确认方案

### 4.3 执行
**必须输出**：修改文件列表 + 编译结果

**执行内容**：
- 创建待办列表跟踪进度
- 按计划修改代码
- 编译验证
- 更新待办状态

**人机协作**：AI 输出执行结果 → 人类执行中反馈（如有）

### 4.4 自检
**必须输出**：完整规则检查表（逐条输出）

**执行内容**：
- 读取 AI_COLLABORATION_SPEC.md 和 CODING_SPEC.md
- 逐条输出所有规则的检查结果
- 消除 IDE 警告
- 确认编译通过

**详细格式**：见 `context/rule/ai-collaboration/checkpoint/CHECKPOINT_SPEC.md`

**人机协作**：AI 输出自检结果 → 人类确认或提问

### 4.5 沉淀
**必须输出**：沉淀内容 + 沉淀路径

**执行内容**：
- 判断沉淀类型（业务/协作）
- 输出场景标签格式
- 等待人类确认后执行

**人机协作**：AI 输出沉淀内容 → 人类确认 → AI 执行

---

## 五、沉淀类型判断

``` text
内容是什么类型？
├─ 协作相关（方法论、沟通方式、错误预防）
│   └─ 谁使用？
│       ├─ AI使用 → .iflow/context/experience/
│       └─ 共用 → .iflow/context/rule/
│
└─ 业务相关（概念、规则、产品需求）
    └─ 谁使用？
        ├─ AI参考 → app-demand/需求/需求冷启动.md
        └─ 人类使用 → app-demand/需求/业务知识/
```

---

## 六、规则来源

| 规范类型 | 文件路径 |
|---------|---------|
| 协作规则 | `@.iflow/context/rule/ai-collaboration/AI_COLLABORATION_SPEC.md ` |
| 编码规则 | `@.iflow/context/rule/ai-coding/CODING_SPEC.md ` |
| 流程规范 | `@.iflow/context/rule/ai-collaboration/workflow/WORKFLOW_SPEC.md ` |
| 检查点规范 | `@.iflow/context/rule/ai-collaboration/checkpoint/CHECKPOINT_SPEC.md ` |

---

**最后更新**：2026-03-04
**版本**：22.0
